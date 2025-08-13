from django.db.models import QuerySet
from django.urls import reverse
from django.contrib import admin, messages
from django.utils.html import format_html
from unfold.admin import (
    ModelAdmin,
)  # Замена from django.contrib import admin.ModelAdmin
from core.apps.retail.models import Supplier, Product, Contact
from .tasks import async_clear_data


@admin.register(Supplier)
class NetworkNodeAdmin(ModelAdmin):
    """
    Admin interface for Supplier models.
    Displays:
    - `pk`
    - `title`
    - `debt`
    - `type_supplier`
    - `supplier_link`
    - `created`
    Filters:
    - `type_supplier`
    - `contact__city`
    Actions:
    - `clear_debt`
    """

    list_display = ("pk", "title", "debt", "type_supplier", "supplier_link", "created")
    list_filter = ("type_supplier", "contact__city")
    actions = ("clear_debt",)

    def supplier_link(self, obj: Supplier):
        """Displays link associated supplier in the adminka"""

        if obj.supplier:
            url = reverse("admin:retail_supplier_change", args=[obj.supplier.id])
            return format_html("<a href='{}'>{}</a>", url, obj.supplier.title)
        return "-"

    supplier_link.short_description = "Поставщик"

    @admin.action(description="Очистить задолженность у выбранных поставщиков")
    def clear_debt(self, request, queryset: QuerySet):
        """
        Action to clear debts from selected suppliers.
        Features:
        - For more than 20 suppliers, launches an async task
        - For smaller quantities, updates the debt sync
        """

        if queryset.count() > 20:
            # Async process for more 20 objects
            supplier_ids = list(queryset.values_list("id", flat=True))
            async_clear_data.delay(supplier_ids)
            self.message_user(
                request, "Задолженность будет очищена для выбранных поставщиков"
            )
        else:
            updated = queryset.update(debt=0.00)
            supplier = "поставщика" if updated == 1 else "поставщиков"
            self.message_user(
                request,
                f"Задолженность очищена у {updated} {supplier}.",
                level=messages.SUCCESS,
            )

    def get_form(self, request, obj=None, **kwargs):
        """
        Config edit form.
        - Allows the creation of new contacts
        - Prohibits changing existing contacts
        - Hides the ability to view contacts
        """
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["contact"].widget.can_add_related = True  # Разрешить создание
        form.base_fields["contact"].widget.can_change_related = (
            False  # Запретить изменение
        )
        form.base_fields["contact"].widget.can_view_related = False  # Скрыть просмотр
        return form


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """
    Admin interface for Product models.
    Displays:
    - `name`
    - `model`
    - `date_product_release`
    """

    list_display = ("name", "model", "date_product_release")


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    """
    Admin interface for Contact models.
    Displays:
    - `country`
    - `city`
    - `street`
    - `house_number`
    - `email` (with a copy button)
    """

    list_display = (
        "country",
        "city",
        "street",
        "house_number",
        "get_email_with_copy",
    )

    def get_email_with_copy(self, obj):
        """Generates  HTML view of an email, with copy button."""

        return format_html(
            """
            <div style="display: flex; align-items: center; gap: 5px;">
                <span>{email}</span>
                <button
                    onclick="
                        var tempInput = document.createElement('textarea');
                        tempInput.value = '{email}';
                        document.body.appendChild(tempInput);
                        tempInput.select();
                        document.execCommand('copy');
                        document.body.removeChild(tempInput);

                        var notice = document.createElement('div');
                        notice.innerHTML = '✓ Email скопирован';
                        notice.style.cssText = [
                            'position: fixed',
                            'top: 20px',
                            'right: 20px',
                            'background: #4CAF50',
                            'color: white',
                            'padding: 10px 15px',
                            'border-radius: 4px',
                            'z-index: 9999',
                            'animation: fadeIn 0.3s, fadeOut 0.3s 1.7s'
                        ].join(';');
                        document.body.appendChild(notice);
                        setTimeout(function(){{
                            notice.remove();
                        }}, 2000);
                    "
                    style="
                        cursor: pointer;
                        background: none;
                        border: none;
                        font-size: 1.2em;
                        padding: 0 5px;
                    "
                    title="Скопировать email"
                >
                    📋
                </button>
            </div>
            <style>
                @keyframes fadeIn {{
                    from {{ opacity: 0; transform: translateY(-10px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                @keyframes fadeOut {{
                    from {{ opacity: 1; transform: translateY(0); }}
                    to {{ opacity: 0; transform: translateY(-10px); }}
                }}
            </style>
            """,
            email=obj.email,
        )

    get_email_with_copy.short_description = "Email"
    get_email_with_copy.allow_tags = True
