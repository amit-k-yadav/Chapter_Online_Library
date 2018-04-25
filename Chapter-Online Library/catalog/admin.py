from django.contrib import admin
from .models import Genre, Book, Language, Author, BookInstance
# Register your models here.

admin.site.register(Genre)
admin.site.register(Language)


#Book Model
class BookInstanceInline(admin.TabularInline): #For inline editing of books
    model = BookInstance
    extra = 0
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'display_genre')
    list_filter = ('title', 'authors')
    inlines = [BookInstanceInline]
admin.site.register(Book, BookAdmin)


#Admin Model
class BookInline(admin.TabularInline):
    model = Book
    extra = 0
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'dob')
    list_filter = ('name','dob')
    fields = ('name', ('dob','dod'))
    inlines = [BookInline]
admin.site.register(Author, AuthorAdmin)


#BookInstance Model
@admin.register(BookInstance) #another way of registeration in admin.py
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('pk','book','language', 'due_back' , 'status', 'borrower')
    list_filter = ('due_back', 'status')
    fieldsets = (('Book Details',{'fields': ('book', 'imprint', 'books_id','language')}),
                 ('Availability',{'fields': ('due_back','status','borrower')}))
#admin.site.register(BookInstance, BookInstanceAdmin)
