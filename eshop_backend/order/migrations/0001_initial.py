# Generated by Django 4.2 on 2023-05-15 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("street", models.CharField(default="", max_length=400)),
                ("city", models.CharField(default="", max_length=50)),
                ("state", models.CharField(default="", max_length=100)),
                ("zip_code", models.CharField(default="", max_length=100)),
                ("phone_no", models.CharField(default="", max_length=20)),
                ("country", models.CharField(default="", max_length=100)),
                ("total_amount", models.IntegerField(default=0)),
                (
                    "payment_status",
                    models.CharField(
                        choices=[("PAID", "Paid"), ("UNPAID", "Unpaid")],
                        default="UNPAID",
                        max_length=20,
                    ),
                ),
                (
                    "status_order",
                    models.CharField(
                        choices=[
                            ("Procesing", "Procesing"),
                            ("Shipped", "Shipped"),
                            ("Delivered", "Delivered"),
                        ],
                        default="Procesing",
                        max_length=40,
                    ),
                ),
                (
                    "payment_mode",
                    models.CharField(
                        choices=[("COD", "Cod"), ("CARD", "Card")],
                        default="COD",
                        max_length=40,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
