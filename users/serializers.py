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


class OTPRegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(trim_whitespace=True)
    otp = serializers.CharField(max_length=6, min_length=4)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    role = serializers.ChoiceField(choices=User.RoleChoices.choices, default=User.RoleChoices.CUSTOMER)
    brand_name = serializers.CharField(max_length=150, required=False, allow_blank=True)


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
            "status",
            "role",
            "groups",
            "is_phone_verified",
            "avatar",
        )

    def get_groups(self, obj):
        return obj.groups.values_list("name", flat=True)

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "national_id", "avatar")


from users.models import Address

class AddressSerializer(serializers.ModelSerializer):
    postal_code = serializers.RegexField(
        r'^\d+$',
        allow_blank=True,
        allow_null=True,
        required=False,
        error_messages={"invalid": "کد پستی فقط باید شامل اعداد باشد."},
    )

    class Meta:
        model = Address
        fields = ("id", "title", "detail", "postal_code", "is_default")
        read_only_fields = ("id",)

from users.models import Notification

class UserNotificationSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.name', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'sender_name', 'message', 'is_read', 'created_at']