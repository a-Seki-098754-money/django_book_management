# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from book_management.models import Member

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    phone_number = forms.CharField(
        max_length=15, 
        required=False,
        help_text="電話番号(ハイフンなし)"
    )
    postal_code = forms.CharField(
        max_length=8, 
        required=False,
        help_text="郵便番号"
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows':3}),
        required=False,
        help_text="住所"
    )
    membership_type = forms.ChoiceField(
        choices=Member.MEMBERSHIP_TYPE_CHOICES,
        initial='regular',
        required=True
    )
    profile_image = forms.ImageField(
        required=False,
        help_text="プロフィール画像"
    )

    class Meta(UserCreationForm.Meta): # ここを修正: UserCreationForm.Metaを継承
        model = User
        # UserCreationForm.Meta.fields に、追加したいUserモデルのフィールドを結合
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Memberオブジェクトを重複なく作成
            Member.objects.get_or_create(
                user=user,
                defaults={
                    'phone_number': self.cleaned_data['phone_number'],
                    'postal_code': self.cleaned_data['postal_code'],
                    'address': self.cleaned_data['address'],
                    'membership_type': self.cleaned_data['membership_type'],
                    'profile_image': self.cleaned_data['profile_image'],
                    'is_active': True
                }
            )
        return user