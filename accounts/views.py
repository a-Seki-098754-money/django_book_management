from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
# パスワード変更のために追加
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        return response
    
# パスワードリセット変更ビュー
class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'accounts/password_change.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "password_change"
        return context

# パスワード変更完了
class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'
    
# パスワード変更用のURLの送付ページ
class PasswordReset(PasswordResetView):
    subject_template_name = 'accounts/mail_template/reset/subject.txt'
    email_template_name = 'accounts/mail_template/reset/message.txt'
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')

# パスワード変更URL送信完了
class PasswordResetDone(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'
    
# 新パスワード入力ページ
class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'

#新パスワード設定完了
class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
