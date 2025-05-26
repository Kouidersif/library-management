from django.contrib import admin
from books.models import Book, Loan, Author
from books.actions import end_loans



@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "page_count", "is_available")
    

        
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "borrower",
        "loan_date",
        "return_date",
        "is_returned",
    )

    actions = [end_loans]
    
    
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")