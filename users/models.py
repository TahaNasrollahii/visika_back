from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from core.models import TimestampedModel

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields) -> "User":
        if not phone_number:
            raise ValueError(_("The Phone Number field must be set"))

        user = User(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_phone_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser, TimestampedModel):
    class GenderChoices(models.IntegerChoices):
        MALE = 1, _("Male")
        FEMALE = 2, _("Female")
        
    username = None

    phone_number = PhoneNumberField(
        verbose_name=_("phone number"),
        default="",
        blank=True,
        unique=True,
        db_index=True,
        region="IR",
    )
        
    class StatusChoices(models.IntegerChoices):
        PENDING = 1, "Pending"
        ACTIVE = 2, "Active"
        BANNED = 3, "Banned"

    class RoleChoices(models.TextChoices):
        CUSTOMER = "customer", _("Customer")
        VENDOR = "vendor", _("Vendor")

    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.PENDING)
    role = models.CharField(max_length=15, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER)

    gender = models.IntegerField(choices=GenderChoices.choices, null=True, blank=True)
    is_phone_verified = models.BooleanField(_("is phone verified"), default=False)
    national_id = models.CharField(max_length=10, blank=True, null=True)
    favorites = models.ManyToManyField('products.Product', related_name='favorited_by', blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)


    objects = UserManager()  # type: ignore

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]
    normalize_fields = ["first_name", "last_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.phone_number})"

    def get_username(self) -> str:
        return str(self.phone_number)


class Address(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    title = models.CharField(max_length=255)
    detail = models.TextField()
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")
        ordering = ["-is_default", "-created_at"]

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.user.phone_number}"

class Vendor(TimestampedModel):
    is_active = models.BooleanField(default=True)
    profile_image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    user = models.OneToOneField(to=User, verbose_name="manager",  on_delete=models.CASCADE, related_name="vendor", null=True, blank=True)

    def __str__(self) -> str:
        return self.name

from django.core.validators import MinValueValidator, MaxValueValidator

class VendorDeliveryRule(TimestampedModel):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, related_name="delivery_rule")
    # Delivery settings
    preparation_days = models.PositiveSmallIntegerField(default=2)
    end_of_order_taking_hour = models.PositiveSmallIntegerField(
        default=15,
        validators=(MinValueValidator(0), MaxValueValidator(24))
    )
    
    # Delivery Days
    saturday = models.BooleanField(default=True)
    sunday = models.BooleanField(default=True)
    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=False)

class Notification(TimestampedModel):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="sent_notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification to {self.recipient.phone_number} from {self.sender.name}"
