from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import donating.models as donating_models

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = donating_models.CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(donating_models.CustomUser, CustomUserAdmin)
admin.site.register(donating_models.Category)
admin.site.register(donating_models.Institution)
admin.site.register(donating_models.Donation)
