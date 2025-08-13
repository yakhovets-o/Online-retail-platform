"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import (
    include,
    path,
)
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from core.apps.retail.views import (
    DebtAboveAverageListView,
    ProductViewSet,
    SupplierByProductViewSet,
    SupplierQRCodeAPIView,
    SupplierViewSet,
)

from .yasg import urlpatterns as doc_urls


router = DefaultRouter()
router.register(r"suppliers", SupplierViewSet, basename="node")
router.register(r"products", ProductViewSet, basename="product")
router.register(
    r"suppliers/by_product", SupplierByProductViewSet, basename="suppliers-by-product"
)


urlpatterns = [
    path("", RedirectView.as_view(url="/admin/", permanent=True)),
    path("admin/", admin.site.urls),
    path("", include("core.apps.users.urls")),
    path("api/", include(router.urls)),
    path("api/statistics/", DebtAboveAverageListView.as_view(), name="statistics"),
    path("api/generate-qr/", SupplierQRCodeAPIView.as_view(), name="generate-qr"),
]

urlpatterns += doc_urls
