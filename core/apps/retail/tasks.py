import random
import qrcode
from decimal import Decimal
from celery import shared_task
from django.core.mail import EmailMessage
from django.core.files.base import ContentFile
from django.db.models import F
from django.conf import settings
from io import BytesIO

from .models import Supplier


@shared_task
def increase_debt():
    """Increases suppliers debt by random number from 5 to 500, every 3 hours."""
    suppliers = Supplier.objects.only("id", "debt")
    for supplier in suppliers:
        amount = Decimal(str(round(random.uniform(5, 500), 2)))
        Supplier.objects.filter(id=supplier.id).update(debt=F("debt") + amount)

    print(f"Долги увеличены у {suppliers.count()} поставщиков")


@shared_task
def decrease_debt():
    """Reduces debt by random number from 100 to 10000 every day at 6:30."""
    suppliers = Supplier.objects.only("id", "debt")

    for supplier in suppliers:
        amount = Decimal(str(round(random.uniform(100, 10000), 2)))
        new_debt = max(Decimal("0"), supplier.debt - amount)
        Supplier.objects.filter(id=supplier.id).update(debt=new_debt)

    print(f"Долги уменьшены у {suppliers.count()} поставщиков")


@shared_task
def async_clear_data(supplier_ids):
    """async clear data for more 20 objects."""
    updated_count = Supplier.objects.filter(id__in=supplier_ids).update(debt=0)
    print(f"Обнулен долг для {updated_count} поставщиков")
    return updated_count


@shared_task
def send_qr_code_email(email, supplier_id):
    """
    Generates and emails supplier contact QR code.

    End-to-end QR code processing:
    - Fetches supplier and contact details
    - Formats contact data for encoding
    - Generates QR code image
    - Emails QR code as PNG attachment

    Parameters:
     - email (str): Recipient email address
     - supplier_id (int): Target supplier ID

    Returns:
    str: Success message or error details

    Error Handling:
    - Catches and returns any exceptions
    - Includes supplier lookup failure
    """
    try:
        supplier = Supplier.objects.get(id=supplier_id)
        contact = supplier.contact

        # data for qr
        contact_data = f"""
        {supplier.title}
        Email: {contact.email}
        Адрес: {contact.country}, {contact.city}, {contact.street}, {contact.house_number}
        """

        # gen qr
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(contact_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # save qr
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_code = ContentFile(buffer.getvalue(), name=f"qr_{supplier_id}.png")

        # send email
        subject = f"QR-код контактов поставщика {supplier.title}"
        message = f"Данные поставщика {supplier.title}:\n{contact_data}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        EmailMessage(
            subject,
            message,
            from_email,
            recipient_list,
            attachments=[(f"qr_{supplier_id}.png", qr_code.read(), "image/png")],
        )

        return f"QR-код отправлен на {email}"
    except Exception as e:
        return f"Ошибка при отправке QR-кода: {str(e)}"
