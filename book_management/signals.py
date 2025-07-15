from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Member
from datetime import date, timedelta

@receiver(post_save, sender=User)
def create_member(sender, instance, created, **kwargs):
    #ユーザー登録時に自動的にMemberを作成
    if created:
        if not hasattr(instance, 'member'):
            try:
                Member.objects.create(
                    user=instance,
                    membership_type='regular',
                    is_active=True,
                    #1年後に期限切れ
                    membership_expity_date = date.today() + timedelta(days=365)
                )
                print(f"Menber created for user: {instance.username}")
            except:
                pass
        
                