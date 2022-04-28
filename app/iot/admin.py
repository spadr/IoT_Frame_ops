from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from iot.models import BooleanModel, CharModel, FloatModel, IntModel, TubeModel, User

# Register your models here.

admin.site.register(TubeModel)
admin.site.register(FloatModel)
admin.site.register(IntModel)
admin.site.register(BooleanModel)
admin.site.register(CharModel)


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("alive_monitoring",)}),
        (_("Permissions"), {"fields": ("is_active", "function_level", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ("email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, MyUserAdmin)
