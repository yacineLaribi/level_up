from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from .models import UserQuest

@receiver(post_save, sender=UserQuest)
def handle_quest_completion(sender, instance, **kwargs):
    if instance.completed and instance.completed_at is None:
        instance.completed_at = datetime.now()
        instance.save()

        # Update user's score and gold
        user = instance.user
        user.score += instance.quest.score_reward
        user.gold += instance.quest.gold_reward

        # Level up logic: Assume each level requires 100 points
        if user.score >= user.level * 100:
            user.level += 1

        user.save()
