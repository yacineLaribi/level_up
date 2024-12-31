from django.contrib import admin
from .models import Clan, ClanMembership , CustomUser

admin.site.register(CustomUser)

from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Clan, ClanMembership , Quest , UserQuest




@admin.register(Clan)
class ClanAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        # Ensure the owner is a saved instance
        if obj.owner and not obj.owner.pk:
            raise ValidationError("The owner must be a saved user before assigning them to the Clan.")

        # Save the Clan instance first
        obj.save()

        # Create ClanMembership if the Clan is newly created
        if not change:
            ClanMembership.objects.create(user=obj.owner, clan=obj)

        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "owner":
            # Restrict the owner field to only show saved users in the form
            kwargs["queryset"] = CustomUser.objects.filter(id__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ClanMembership)
class ClanMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'clan', 'joined_at')
    search_fields = ('user__username', 'clan__name')



@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'score_reward', 'gold_reward', 'is_special', 'created_at')
    search_fields = ['name']  # Corrected: Made this a list
    list_filter = ['is_special', 'created_at']  # Corrected: Made this a list

@admin.register(UserQuest)
class UserQuestAdmin(admin.ModelAdmin):
    list_display = ('user', 'quest', 'completed', 'completed_at')
    search_fields = ['user__username', 'quest__name']  # Corrected: Made this a list
    list_filter = ['completed']  # Corrected: Made this a list