from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    isbn = models.CharField(max_length=13, unique=True, null=True,blank=True,help_text="ISBNコード（重複不可、空白不可）")
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200)
    publication_date = models.DateField()
    category = models.CharField(max_length=50, null=True, blank=True)
    # 画像フィールド
    cover_image = models.ImageField(
        upload_to='book_covers',
        null=True,
        blank=True,
        help_text="図書の表紙画像"
        )
    
    #基本情報
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    description = models.TextField(null=True, blank=True,help_text="図書の概要")
    
    #レビュー関連のデータフィールド
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        help_text="平均評価"
    )
    review_count = models.PositiveIntegerField(default=0, help_text="レビュー数")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def update_rating(self):
        #レビューの平均評価の更新
        reviews = self.review_set.all()
        if reviews:
            self.average_rating = sum([r.rating for r in reviews]) / len(reviews)
            self.review_count = len(reviews)
        else:
            self.average_rating = 0.00
            self.review_count = 0
        self.save()

class Member(models.Model):
    MEMBERSHIP_TYPE_CHOICES = [
        ('regular', '一般会員'),
        ('student', '学生会員'),
        ('staff', 'スタッフ'),
        ('premium', 'プレミアム会員'), 
    ]
    
    member_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    #連絡先情報
    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        help_text="電話番号（ハイフンなし）"
    )
    
    #住所情報
    postal_code = models.CharField(
        max_length=8,
        null=True,
        blank=True,
        help_text="郵便番号"
    )
    address = models.TextField(
        null=True,
        blank=True,
        help_text="住所"
    )
    
    #会員情報
    membership_type = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_TYPE_CHOICES,
        default='regular'
    )
    membership_start_date = models.DateField(auto_now_add=True)
    membership_expity_date = models.DateField(null=True, blank=True)
    
    #プロフィール画像
    profile_image = models.ImageField(
        upload_to='member_profiles/',
        null=True,
        blank=True,
        help_text="プロフィール画像"
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.get_membership_type_display()})"
    
#貸し出しテーブル   
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    
    #レビュー内容
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(5)],
        help_text="1-5の評価"
    )
    title = models.CharField(max_length=100, help_text="レビュータイトル")
    content = models.TextField(help_text="レビュー内容")
    
    #いいね機能
    likes = models.ManyToManyField(
        Member,
        related_name='liked_reviews',
        blank=True,
        help_text="このレビューにいいねした会員"
    )
    
    #ステータス
    is_approved = models.BooleanField(default=True, help_text="承認済み")
    is_featured = models.BooleanField(default=True, help_text="おすすめレビュー")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('book', 'member') #1人1冊につき1つのレビュー
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.book.title} - {self.member.user.username} ({self.rating}★)"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        #レビュー保存時に図書の平均評価を更新
        self.book.update_rating()
        
class Rental(models.Model):
    RENTAL_STATUS_CHOICES = [
        ('borrowed', '貸出中'),
        ('returned', '返却済み'),
        ('overdue', '延滞'),
    ]
    
    rental_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    rental_date = models.DateTimeField(auto_now_add=True)
    return_due_date = models.DateField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=RENTAL_STATUS_CHOICES, default='borrowed')
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.book.title} - {self.member.user.username}"