# book_management/forms.py
from django import forms
from .models import Review # Reviewモデルをインポート
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
