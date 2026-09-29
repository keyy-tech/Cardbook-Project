from rest_framework import serializers

from .models import Card


class ShortCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [  
            "id",
            "card_type",
            "card_name",
            "card_number",
            "expiry_date",
        ]

        read_only_fields = [  
            "id",
        ]


class FullCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [  
            "id",
            "card_type",
            "card_name",
            "card_number",
            "issue_date",
            "expiry_date",
            "issuing_authority",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ] 