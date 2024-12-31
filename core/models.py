from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    
    score = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    gold = models.IntegerField(default=1000)

    email = models.EmailField(unique=True)  
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'


from django.core.exceptions import ValidationError
from django.conf import settings

class Clan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owned_clans")

    def __str__(self):
        return self.name
    
    # def clean(self):
    #     """Ensure a clan does not have more than 50 members."""
    #     # Use the queryset to count the number of members
    #     if ClanMembership.objects.filter(clan=self).count() >= 50:
    #         raise ValidationError('A clan cannot have more than 50 members.')
    class Meta:
        verbose_name = "Clan"
        verbose_name_plural = "Clans"


class ClanMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clan = models.ForeignKey(Clan, related_name="members", on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'clan')  # Ensure a user can join a clan only once

    def __str__(self):
        return f'{self.user.username} - {self.clan.name}'


class Quest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    score_reward = models.IntegerField()  # Score awarded for completing the quest
    gold_reward = models.IntegerField(default=0)  # Optional gold reward
    is_special = models.BooleanField(default=False)  # Special quest flag
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserQuest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_quests")
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name="user_quests")
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.quest.name}"