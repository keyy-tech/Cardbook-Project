from rest_framework import serializers
from . models import Users


class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
    )

    class Meta:
        model = Users
        fields = [
            "email",
            "password",
            "first_name",
            "last_name"
        ]


    def create(self, validated_data):
        user = Users.objects.create_user(
            **validated_data
            )
        
        return user



class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    submitted_code = serializers.CharField()
    new_password = serializers.CharField()

