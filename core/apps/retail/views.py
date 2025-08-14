from django.db.models import Avg
from rest_framework import (
    generics,
    permissions,
    status,
    views,
    viewsets,
)
from rest_framework.response import Response

from .models import (
    Product,
    Supplier,
)
from .serializers import (
    ProductSerializer,
    SupplierQRRequestSerializer,
    SupplierSerializer,
)
from .tasks import send_qr_code_email


class SupplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint managing suppliers with country-based filtering.
    Implements CRUD for suppliers, only authenticated users.

    Features:
    - Uses select_related for contact to optimize queries
    - Uses prefetch_related for employees and retail
    - Returns empty queryset if no country parameter provided
    """

    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        country = self.request.query_params.get("country")
        if not country:
            return Supplier.objects.none()
        return (
            Supplier.objects.select_related("contact")
            .prefetch_related("employees", "products")
            .filter(contact__country__iexact=country, employees=self.request.user)
        )


class DebtAboveAverageListView(generics.ListAPIView):
    """
    API endpoint returns suppliers with debt above average.
    Only authenticated users, available read-only of suppliers.
    Includes query optimization with select_related and prefetch_related.
    """

    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        avg_debt = Supplier.objects.aggregate(avg_debt=Avg("debt"))["avg_debt"]
        print(f"Current user: {self.request.user}")
        return (
            Supplier.objects.select_related("contact")
            .prefetch_related("employees", "products")
            .filter(debt__gt=avg_debt, employees__in=[self.request.user])
        )


class SupplierByProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint returns suppliers by product ID
    Only authenticated users, available read-only of suppliers.

    Returns empty queryset if:
    - No product_id provided
    - Invalid product_id format
    - No matching suppliers found
    """

    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        product_id = self.request.query_params.get("product_id")

        if not product_id:
            return Supplier.objects.none()

        try:
            product_id = int(product_id)
        except (TypeError, ValueError):
            return Supplier.objects.none()

        return (
            Supplier.objects.filter(
                products__id=product_id, employees=self.request.user
            )
            .select_related("contact")
            .prefetch_related("employees", "products")
        )


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint returns retail.
    Implements CRUD for retail, only authenticated users.
    """

    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer


class SupplierQRCodeAPIView(views.APIView):
    """
    API endpoint generating and emailing supplier QR codes.

    Accepts POST requests with:
    - `supplier_id`: ID of the supplier
    - `email`: Recipient email address

    Processes the request asynchronously via Celery task.
    Returns immediate response indicating task initiation.

    Responses:
    - `202 Accepted`: Task started successfully
    - `400 Bad Request`: Invalid input data
    - `404 Not Found`: Supplier not found
    """

    def post(self, request):
        serializer = SupplierQRRequestSerializer(data=request.data)
        if serializer.is_valid():
            supplier_id = serializer.validated_data["supplier_id"]
            email = serializer.validated_data["email"]

            try:
                send_qr_code_email.delay(email, supplier_id)
                return Response(
                    {"status": "QR code generation and email sending started"},
                    status=status.HTTP_202_ACCEPTED,
                )
            except Supplier.DoesNotExist:
                return Response(
                    {"error": "Supplier not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
