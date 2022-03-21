from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import serializers

User = get_user_model()


class CreateNewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(email=validated_data["email"], password=validated_data["password"])

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def validate_password(self, value):
        """Validates that a password is:
        - at least 8 characters long
        - has 1 digit and 1 letter
        """
        min_length = 8

        if len(value) < min_length:
            raise serializers.ValidationError("Password must be at least {min_length} characters")

        # check for digit
        if not any(char.isdigit() for char in value):
            raise ValidationError("Password must contain at least 1 digit.")

        # check for letter
        if not any(char.isalpha() for char in value):
            raise ValidationError("Password must contain at least 1 letter.")

        return value
