# book_management/management/commands/create_missing_members.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from book_management.models import Member

class Command(BaseCommand):
    help = 'Creates Member objects for existing Users who do not have one.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Checking for missing Member objects...'))
        
        users_without_member = []
        for user in User.objects.all():
            if not hasattr(user, 'member'):
                users_without_member.append(user)
        
        if not users_without_member:
            self.stdout.write(self.style.SUCCESS('All existing Users already have a Member object.'))
            return

        created_count = 0
        for user in users_without_member:
            try:
                Member.objects.create(
                    user=user,
                    membership_type='regular', # デフォルトの会員タイプ
                    is_active=True
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created Member for user: {user.username}'))
                created_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create Member for user {user.username}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'Finished. Created {created_count} new Member objects.'))
