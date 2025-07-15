# book_management/admin.py
from django.contrib import admin
from .models import Book, Member, Rental, Review

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # 一覧画面で表示する項目
    list_display = (
        'title', 
        'author', 
        'publisher', 
        'isbn', 
        'category',
        'available_copies', 
        'total_copies',
        'average_rating',
        'review_count',
        'publication_date'
    )
    
    # フィルター機能
    list_filter = (
        'category', 
        'publisher', 
        'publication_date',
        'created_at'
    )
    
    # 検索機能
    search_fields = (
        'title', 
        'author', 
        'publisher',
        'isbn',
        'category'
    )
    
    # 読み取り専用フィールド
    readonly_fields = (
        'average_rating', 
        'review_count', 
        'created_at', 
        'updated_at'
    )
    
    # 編集画面のフィールド配置
    fieldsets = (
        ('基本情報', {
            'fields': (
                'title', 
                'author', 
                'publisher', 
                'isbn', 
                'publication_date', 
                'category'
            )
        }),
        ('詳細情報', {
            'fields': (
                'description', 
                'cover_image'
            ),
            'classes': ('collapse',)  # 折りたたみ可能
        }),
        ('在庫管理', {
            'fields': (
                'total_copies', 
                'available_copies'
            )
        }),
        ('レビュー情報', {
            'fields': (
                'average_rating', 
                'review_count'
            ),
            'classes': ('collapse',)
        }),
        ('システム情報', {
            'fields': (
                'created_at', 
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    # 一覧画面での並び順
    ordering = ('-created_at',)
    
    # ページネーション
    list_per_page = 20
    
    # 一覧画面で編集可能なフィールド
    list_editable = ('available_copies',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'membership_type', 
        'phone_number', 
        'is_active', 
        'created_at'
    )
    
    list_filter = (
        'membership_type', 
        'is_active',
        'created_at'
    )
    
    search_fields = (
        'user__username', 
        'user__email', 
        'user__first_name',
        'user__last_name',
        'phone_number'
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('ユーザー情報', {
            'fields': ('user', 'membership_type')
        }),
        ('連絡先情報', {
            'fields': (
                'phone_number', 
                'postal_code', 
                'address'
            )
        }),
        ('プロフィール', {
            'fields': ('profile_image',),
            'classes': ('collapse',)
        }),
        ('ステータス', {
            'fields': ('is_active',)
        }),
        ('システム情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-created_at',)
    list_per_page = 25

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = (
        'book', 
        'member', 
        'rental_date', 
        'return_due_date', 
        'return_date', 
        'status',
        'fine_amount'
    )
    
    list_filter = (
        'status', 
        'rental_date', 
        'return_due_date',
        'return_date'
    )
    
    search_fields = (
        'book__title', 
        'member__user__username',
        'book__author'
    )
    
    readonly_fields = (
        'rental_date', 
        'created_at', 
        'updated_at'
    )
    
    fieldsets = (
        ('貸出情報', {
            'fields': (
                'book', 
                'member', 
                'rental_date'
            )
        }),
        ('返却情報', {
            'fields': (
                'return_due_date', 
                'return_date', 
                'status'
            )
        }),
        ('料金・備考', {
            'fields': (
                'fine_amount', 
                'notes'
            ),
            'classes': ('collapse',)
        }),
        ('システム情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-rental_date',)
    list_per_page = 30
    
    # ステータスを一覧画面で編集可能に
    list_editable = ('status',)
    
    # 日付フィルター
    date_hierarchy = 'rental_date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'book', 
        'member', 
        'rating', 
        'title', 
        'is_approved', 
        'is_featured',
        'created_at'
    )
    
    list_filter = (
        'rating', 
        'is_approved', 
        'is_featured',
        'created_at'
    )
    
    search_fields = (
        'book__title', 
        'member__user__username', 
        'title',
        'content'
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('レビュー基本情報', {
            'fields': (
                'book', 
                'member', 
                'rating'
            )
        }),
        ('レビュー内容', {
            'fields': (
                'title', 
                'content'
            )
        }),
        ('ステータス', {
            'fields': (
                'is_approved', 
                'is_featured'
            )
        }),
        ('いいね', {
            'fields': ('likes',),
            'classes': ('collapse',)
        }),
        ('システム情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-created_at',)
    list_per_page = 25
    
    # 承認状態を一覧画面で編集可能に
    list_editable = ('is_approved', 'is_featured')
    
    # 多対多フィールドの表示を改善
    filter_horizontal = ('likes',)

# 管理画面のタイトルをカスタマイズ
admin.site.site_header = "図書管理システム 管理画面"
admin.site.site_title = "図書管理システム"
admin.site.index_title = "管理メニュー"

# book_management/admin.py
# from django.contrib import admin
# from .models import Book, Member, Rental, Review

# # シンプルに登録（エラーが出ない）
# # admin.site.register(Book)
# admin.site.register(Member)
# admin.site.register(Rental)
# admin.site.register(Review)

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'publisher', 'isbn', 'category', 
#                     'available_copies', 'total_copies', 
#                     'average_rating', 'review_count', 'publication_date')