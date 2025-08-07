# book_management/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Member # Reviewモデルをインポート
from .models import Book

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        # ここを正確に修正してください
        fields = ['rating', 'title', 'content'] # 'comment' や 'ranking' は含めない
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'レビューのタイトル'}),
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'レビュー内容'}),
        }
        labels = {
            'rating': '評価',
            'title': 'タイトル',
            'content': 'レビュー内容',
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'publisher', 'publication_date', 'category',
            'cover_image', 'total_copies', 'available_copies', 'description'
        ]
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
            
    def save(self, commit=True):
        user= super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# 修正: ProfileEditFormはUserモデル用
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User  # Userモデルに変更
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': '名前',
            'last_name': '姓',
            'email': 'メールアドレス',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),  # 'from-control'を'form-control'に修正
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),   # 'from-control'を'form-control'に修正
            'email': forms.EmailInput(attrs={'class': 'form-control'}),      # 'from-control'を'form-control'に修正
        }

class MemberEditForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['phone_number', 'address']
        labels = {
            'phone_number': '電話番号',
            'address': '住所',
        }
        widgets = {
          'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
          'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }