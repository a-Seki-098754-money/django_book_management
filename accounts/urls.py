from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    # パスワード変更の際追加
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    #パスワードリセットの時に追加
    path('password_reset/', views.PasswordReset.as_view(),name='password_reset'),
    path('password_reset/done', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(),name='password_reset_confirm'),
    path('reset/done/',views.PasswordResetComplete.as_view(),name='password_reset_complete'),
    
]
