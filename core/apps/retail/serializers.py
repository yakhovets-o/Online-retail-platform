from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.apps.retail.models import (
    Contact,
    Product,
    Supplier,
)


User = get_user_model()


class SupplierQRRequestSerializer(serializers.Serializer):
    """
    Serializer handling QR code generation requests for suppliers.

    Used when requesting to generate a QR code for a specific supplier.
    Validates:
    - supplier_id - valid integer
    - email - properly formatted email address
    """

    supplier_id = serializers.IntegerField()
    email = serializers.EmailField()


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer User model.

    Handles serialization user information:
    - `id`
    - `username`
    - `email`
    - `first_name`
    - `last_name`
    """

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer Contact model.

    Handles serialization contact information:
    - `email`
    - `country`
    - `city`
    - `street`
    - `house_number`
    """

    class Meta:
        model = Contact
        fields = ("email", "country", "city", "street", "house_number")


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer Product model.

    Handles serialization product information:
    - `name`
    - `model`
    - `date_product_release`
    """

    class Meta:
        model = Product
        fields = ("name", "model", "date_product_release")


class SupplierSerializer(serializers.ModelSerializer):
    """
    Serializer Supplier model with nested relationships.

    Includes:
    - contact
    - retail (read-only)
    - employees (read-only)

    Note:
    - debt (read-only)
    - retail and employees (read-only)

    Handles serialization supplier information:
    - `title`
    - `type_supplier`
    - `debt`
    - `supplier`
    - `retail`
    - `employees`
    - `contact`
    """

    contact = ContactSerializer()
    products = ProductSerializer(many=True, read_only=True)
    employees = ClientSerializer(many=True, read_only=True)

    class Meta:
        read_only_fields = ("debt",)
        model = Supplier
        fields = (
            "title",
            "type_supplier",
            "debt",
            "supplier",
            "retail",
            "employees",
            "contact",
        )
