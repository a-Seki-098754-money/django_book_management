# book_management/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db import IntegrityError
from datetime import date, timedelta, datetime 
from .models import Book, Member, Rental, Review
from .forms import ReviewForm, BookForm, ProfileEditForm, MemberEditForm
from . import mail
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    """トップページ"""
    books = Book.objects.all()[:6]  # 最新6冊を表示
    context = {
        'books': books,
    }
    return render(request, 'book_management/index.html', context)

def book_list(request):
    """図書一覧ページ"""
    books = Book.objects.all().order_by('-created_at')
    context = {
        'books': books,
    }
    return render(request, 'book_management/book_list.html', context)

def book_detail(request, pk): 
    """図書詳細ページ"""
    book = get_object_or_404(Book, pk=pk) 
    reviews = book.review_set.filter(is_approved=True).order_by('-created_at')
    
    user_review = None
    if request.user.is_authenticated:
        try:
            member = Member.objects.get(user=request.user)
            user_review = Review.objects.get(book=book, member=member)
        except (Member.DoesNotExist, Review.DoesNotExist):
            pass
            
    context = {
        'book': book,
        'reviews': reviews,
        'user_review': user_review,
    }
    return render(request, 'book_management/book_detail.html', context)

@login_required
def borrow_book(request, pk): 
    """図書貸出処理"""
    book = get_object_or_404(Book, pk=pk) 
    
    if request.method == 'POST':
        try:
            member = Member.objects.get(user=request.user)
            
            if book.available_copies > 0:
                existing_rental = Rental.objects.filter(
                    book=book, 
                    member=member, 
                    status='borrowed'
                ).exists()
                
                if not existing_rental:
                    rental = Rental.objects.create(
                        book=book,
                        member=member,
                        return_due_date=date.today() + timedelta(days=14)
                    )
                    
                    book.available_copies -= 1
                    book.save()
                    
                    messages.success(request, f'「{book.title}」を貸し出しました。返却期限は{rental.return_due_date}です。')
                    
                    # メール通知
                    subject = f'図書貸し出し完了のお知らせ: {book.title}'
                    body_html = (
                        f'<p>{request.user.username}様</p>'
                        f'<p>「<strong>{book.title}</strong>」の貸し出しが完了しました。</p>'
                        f'<ul>'
                        f'<li>貸出日: {rental.rental_date.strftime("%Y年%m月%d日 %H時%M分")}</li>'
                        f'<li>返却期限: {rental.return_due_date.strftime("%Y年%m月%d日")}</li>'
                        f'</ul>'
                        f'<p>期限までに返却をお願いいたします。</p>'
                        f'<p>図書管理システム</p>'
                    )
                    
                    recipient_email = [request.user.email]
                    if mail.send_mail(recipient_email, subject, body_html):
                        messages.info(request, '貸出確認メールを送信しました。')
                    else:
                        messages.error(request, 'メール送信に失敗しました。')
                else:
                    messages.error(request, 'この図書は既に借りています。')
            else:
                messages.error(request, 'この図書は現在貸出中です。')
                
        except Member.DoesNotExist:
            messages.error(request, '会員登録が必要です。')
    return redirect('book_management:book_detail', pk=pk) # ここを修正

@login_required
def return_book(request, pk): 
    """図書返却処理"""
    book = get_object_or_404(Book, pk=pk) 
    
    if request.method == 'POST':
        try:
            member = Member.objects.get(user=request.user)
            rental = get_object_or_404(
                Rental, 
                book=book, 
                member=member, 
                status='borrowed'
            )
            
            rental.return_date = datetime.now()
            rental.status = 'returned'
            rental.save()
            
            book.available_copies += 1
            book.save()
            
            messages.success(request, f'「{book.title}」を返却しました。')
                
        except Member.DoesNotExist:
            messages.error(request, '会員登録が必要です。')
        except Rental.DoesNotExist:
            messages.error(request, 'この図書の貸出記録が見つかりません。')
    return redirect('book_management:book_detail', pk=pk) # ここを修正

@login_required
def my_rentals(request):
    """自分の貸出履歴"""
    try:
        member = Member.objects.get(user=request.user)
        rentals = Rental.objects.filter(member=member).order_by('-rental_date')
        
        context = {
            'rentals': rentals,
        }
        return render(request, 'book_management/my_rentals.html', context)
            
    except Member.DoesNotExist:
        messages.error(request, '会員登録が必要です。')
        return redirect('book_management:index') # ここを修正

@login_required
def add_review(request, pk): 
    """レビュー追加"""
    book = get_object_or_404(Book, pk=pk) 
    
    try:
        member = Member.objects.get(user=request.user) 
    except Member.DoesNotExist:
        messages.error(request, '会員登録が必要です。')
        return redirect('book_management:book_detail', pk=book.pk) # ここを修正

    existing_review = Review.objects.filter(book=book, member=member).first() 
    if existing_review:
        form = ReviewForm(request.POST or None, instance=existing_review)
        message = "この本のレビューは既に投稿されています。編集してください。"
    else:
        form = ReviewForm(request.POST or None)
        message = None

    if request.method == 'POST':
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.member = member 
            try:
                review.save()
                messages.success(request, 'レビューを投稿しました！')
                return redirect('book_management:book_detail', pk=book.pk) # ここを修正
            except IntegrityError:
                form.add_error(None, "既にこの本にレビューを投稿しています。")
        
    context = {
        'book': book,
        'form': form, 
        'message': message,
    }
    return render(request, 'book_management/add_review.html', context)

def search_books(request):
    """図書検索"""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    books = Book.objects.all()
    
    if query:
        books = books.filter(
            title__icontains=query
        ) | books.filter(
            author__icontains=query
        ) | books.filter(
            publisher__icontains=query
        )
    if category:
        books = books.filter(category=category)
    books = books.order_by('-created_at')
    
    categories = Book.objects.values_list('category', flat=True).distinct()
    categories = [cat for cat in categories if cat]  
    
    context = {
        'books': books,
        'query': query,
        'category': category,
        'categories': categories,
    }
    return render(request, 'book_management/search_results.html', context)

def test_view(request):
    """テスト用ビュー"""
    return HttpResponse("テストページが正常に表示されました！")

def add_book(request):
    if not request.user.is_staff:
        return HttpResponse('権限がありません', status=403)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '図書を追加しました。')
            return redirect('book_management:index')
    else:
        form = BookForm()
    return render(request, 'book_management/book_form.html', {'form': form})

def edit_book(request, pk):
    if not request.user.is_staff:
        return HttpResponse('権限がありません', status=403)
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, '図書情報を更新しました。')
            return redirect('book_management:index')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_management/book_form.html', {'form': form})

def delete_book(request, pk):
    if not request.user.is_staff:
        return HttpResponse('権限がありません', status=403)
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, '図書を削除しました。')
        return redirect('book_management:index')
    return render(request, 'book_management/book_confirm_delete.html', {'book': book})

@login_required
def profile_view(request):
    """プロフィールページ"""
    try:
        member = request.user.member
    except Member.DoesNotExist:
        member = None
        
    context = {
        'user': request.user,
        'member': member,
        'membership_level':member.get_membership_level_display() if member else '未設定',
    }
    return render(request, 'book_management/profile.html', context)

@login_required
def profile_edit(request):
    """プロフィール編集"""
    try:
        member = request.user.member
    except Member.DoesNotExist:
        # 会員登録がない場合は新規作成
        member = Member.objects.create(user=request.user)
        
    if request.method == 'POST':
        user_form = ProfileEditForm(request.POST, instance=request.user)  # request.userを渡す
        member_form = MemberEditForm(request.POST, instance=member)       # memberを渡す
        
        if user_form.is_valid() and member_form.is_valid():
            user_form.save()
            member_form.save()
            messages.success(request, 'プロフィールが更新されました。')
            return redirect('book_management:profile')
    else:
        # 正しいインスタンスを返す
        user_form = ProfileEditForm(instance=request.user)  # request.userを渡す
        member_form = MemberEditForm(instance=member)       # memberを渡す
            
    context = {
        'user_form': user_form,
        'member_form': member_form,
    }
    return render(request, 'book_management/profile_edit.html', context)
