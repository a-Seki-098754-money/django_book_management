# book_management/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Member, Rental # Rentalをインポート

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance)
    # ユーザーが更新された場合でもMemberオブジェクトが存在することを確認
    instance.member.save()

# 新しく追加: レンタル履歴に基づいて会員ランクを更新するシグナル
@receiver(post_save, sender=Rental)
@receiver(post_delete, sender=Rental) # レンタルが削除された場合も考慮
def update_membership_level(sender, instance, **kwargs):
    user = instance.member.user
    member = instance.member
    
    # そのユーザーの完了したレンタル数をカウント
    # 返却日が設定されているレンタルのみをカウントする
    completed_rentals_count = Rental.objects.filter(
        member=member, 
        return_date__isnull=False # 返却日が設定されているもの
    ).count()
    
    # 貸出中のものもカウントに含める場合は以下も追加
    # current_rentals_count = Rental.objects.filter(
    #     member=member,
    #     return_date__isnull=True
    # ).count()
    # total_rentals_count = completed_rentals_count + current_rentals_count

    # 貸し借り回数が10回以上ならプレミアム会員
    if completed_rentals_count >= 10:
        if member.membership_level != 'Premium':
            member.membership_level = 'Premium'
            member.save()
            print(f"{user.username} はプレミアム会員になりました！") # デバッグ用
    else:
        if member.membership_level != 'Standard':
            member.membership_level = 'Standard'
            member.save()
            print(f"{user.username} はスタンダード会員になりました。") # デバッグ用