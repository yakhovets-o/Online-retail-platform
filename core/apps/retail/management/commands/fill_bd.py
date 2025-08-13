import random
from faker import Faker
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.apps.retail.models import Supplier, Contact, Product, SupplierChoices

User = get_user_model()
fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Fill database with fake suppliers data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--suppliers", type=int, default=50, help="Number of suppliers to create"
        )
        parser.add_argument(
            "--products", type=int, default=20, help="Number of products to create"
        )
        parser.add_argument(
            "--users", type=int, default=10, help="Number of users to create"
        )

    def handle(self, *args, **options):
        suppliers_count = options["suppliers"]
        products_count = options["products"]
        users_count = options["users"]

        self.stdout.write("Starting data generation...")

        # Создаем пользователей
        self.stdout.write(f"Creating {users_count} users...")
        users = []
        for _ in range(users_count):
            user = User.objects.create_user(
                username=fake.user_name(), email=fake.email(), password="testpass123"
            )
            users.append(user)

        # Создаем продукты
        self.stdout.write(f"Creating {products_count} products...")
        products = []
        for _ in range(products_count):
            product = Product.objects.create(
                name=fake.word().capitalize(),
                model=fake.bothify(text="??-####"),
                date_product_release=timezone.make_aware(fake.date_time_this_decade()),
            )
            products.append(product)

        # Создаем контакты (на 20% больше чем поставщиков)
        contacts_count = int(suppliers_count * 1.2)
        self.stdout.write(f"Creating {contacts_count} contacts...")

        # Создаем поставщиков с иерархией
        self.stdout.write(f"Creating {suppliers_count} suppliers with hierarchy...")
        suppliers = []
        for i in range(suppliers_count):
            # Определяем тип поставщика (0 - Завод, 1 - Розничная сеть, 2 - ИП)
            if i == 0:
                # Первый поставщик - всегда завод
                supplier_type = SupplierChoices.FACTORY
                parent = None
            else:
                supplier_type = random.choice(
                    [
                        SupplierChoices.DEALERSHIP_CENTER,
                        SupplierChoices.INDIVIDUAL_ENTREPRENEUR,
                    ]
                )
                # Выбираем родителя из уже созданных поставщиков
                parent = random.choice(suppliers) if suppliers else None
            contact = Contact.objects.create(
                email=fake.email(),
                country=fake.country(),
                city=fake.city(),
                street=fake.street_name(),
                house_number=fake.building_number(),
            )

            supplier = Supplier.objects.create(
                title=fake.company(),
                type_supplier=supplier_type,
                debt=round(random.uniform(0, 10000), 2),
                contact=contact,
                supplier=parent,
            )

            # Добавляем случайных сотрудников (1-3) и продукты (1-5)
            supplier.employees.set(random.sample(users, random.randint(1, 3)))
            supplier.products.set(random.sample(products, random.randint(1, 5)))

            suppliers.append(supplier)

            self.stdout.write(f"Created supplier: {supplier} (level: {supplier.level})")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created:\n"
                f"- {users_count} users\n"
                f"- {products_count} products\n"
                f"- {contacts_count} contacts\n"
                f"- {suppliers_count} suppliers"
            )
        )
