from django.contrib import admin

# Register your models here.
from .models import *


admin .site .register (Genre)
admin .site .register (Tag)

# admin .site .register (BookOrder)
admin .site .register (Author)
admin .site .register (Feedback)
admin .site .register (WishList)
admin.site.register(FavoriteAuthor)



class BookOrderAdmin(admin.ModelAdmin):
    list_display=('book','user','status')
    list_display_links=('book','user','status')
    list_filter=[
        ('status',admin.ChoicesFieldListFilter),
        ('is_paid',admin.BooleanFieldListFilter),
        ('created_at',admin.DateFieldListFilter),
        ('user',admin.RelatedFieldListFilter),
    ]

admin.site.register(BookOrder,BookOrderAdmin)

class BookAdmin(admin.ModelAdmin):
    # list_display=('title','author','price')
    # list_display_links=('title','author','price')
    list_filter=[
        ('author',admin.RelatedOnlyFieldListFilter),
        # ('price',admin.),
    ]

admin .site .register (Book,BookAdmin)