from django.conf import settings
from django.db import models


class Card(models.Model):

    class CardType(models.TextChoices):
        GHANA_CARD = "ghana_card", "Ghana Card"
        DRIVERS_LICENSE = "drivers_license", "Driver's License"
        STUDENT_ID = "student_id", "Student ID"
        PASSPORT = "passport", "Passport"
        OTHER = "other", "Other"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cards"
    )

    card_type = models.CharField(
        max_length=50,
        choices=CardType.choices
    )

    card_name = models.CharField(max_length=100)

    card_number = models.CharField(max_length=100)

    issue_date = models.DateField(
        null=True,
        blank=True
    )

    expiry_date = models.DateField(
        null=True,
        blank=True
    )

    issuing_authority = models.CharField(
        max_length=150,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.card_name