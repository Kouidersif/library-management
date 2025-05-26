from django.contrib import admin
from books.models import Book, Loan, Author




admin.site.register(Book)
admin.site.register(Loan)
admin.site.register(Author)