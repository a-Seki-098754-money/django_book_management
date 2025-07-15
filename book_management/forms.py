# book_management/forms.py
from django import forms
from .models import Review # Reviewモデルをインポート

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
