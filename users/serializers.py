from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(trim_whitespace=True)
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
        )
        return user
    
    
class OTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(trim_whitespace=True)


class OTPLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(trim_whitespace=True)
    otp = serializers.CharField(max_length=6, min_length=4)


class UserInfoSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "national_id",
            "birth_date",
            "status",
            "groups",
            "is_phone_verified",
        )

    def get_groups(self, obj):
        return obj.groups.values_list("name", flat=True)

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "national_id", "birth_date")