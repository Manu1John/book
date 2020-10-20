from django.contrib import admin
from .models import books,Registerbook,Wishlist
# Register your models here.

class BooksAdmin(admin.ModelAdmin):
    list_display= ('book_name', 'author', 'category', 'quantity', 'language', 'pages', 'book_published', 'summary')
admin.site.register(books)



admin.site.register(Registerbook)
admin.site.register(Wishlist)