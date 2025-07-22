# book_management/urls.py
from django.urls import path
from . import views

app_name = 'book_management' # アプリケーションの名前空間を定義 (もし未定義なら追加)

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'), # pk に統一
    path('books/<int:pk>/borrow/', views.borrow_book, name='borrow_book'), # pk に統一
    path('books/<int:pk>/return/', views.return_book, name='return_book'), # pk に統一
    path('books/<int:pk>/review/', views.add_review, name='add_review'), # pk に統一
    path('my_rentals/', views.my_rentals, name='my_rentals'),
    path('search/', views.search_books, name='search_books'),
    path('test/', views.test_view, name='test_view'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
]