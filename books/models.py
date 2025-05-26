from django.db import models
from django.conf import settings
from BookLibrariBackend.models import BaseModel
from books.managers import BooksQuerysetManager, LoansQuerysetManager

class Author(BaseModel):
    first_name = models.CharField(max_length=100, help_text="Enter the author's first name.")
    last_name = models.CharField(max_length=100, help_text="Enter the author's last name.")
    avatar = models.FileField(
        upload_to="authors", null=True, blank=True, help_text="Upload an avatar image."
    )
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name



class Book(BaseModel):
    title = models.CharField(max_length=200, help_text="Enter the title of the book.")
    author = models.ForeignKey(
        Author, on_delete=models.PROTECT, help_text="Select the author of the book."
    )
    isbn = models.CharField(
        max_length=13, unique=True, help_text="Enter the 13-character ISBN number."
    )
    page_count = models.PositiveIntegerField(help_text="Enter the number of pages.")
    is_available = models.BooleanField(default=True)
    
    objects = BooksQuerysetManager.as_manager()

    class Meta:
        ordering = ["title"]
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"{self.title} by {self.author.full_name}"


class Loan(BaseModel):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, help_text="Enter the book to be borrowed."
    )
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="loans",
        help_text="Enter the borrower's username.",
    )
    loan_date = models.DateField(
        auto_now_add=True, help_text="The date the book was borrowed."
    )
    return_date = models.DateField(
        null=True, blank=True, help_text="The date the book is expected to be returned."
    )
    is_returned = models.BooleanField(
        default=False, help_text="Has the book been returned?"
    )
    
    objects = LoansQuerysetManager.as_manager()
    
    class Meta:
        verbose_name = "Loan"
        verbose_name_plural = "Loans"
        ordering = ["-loan_date"]

    def __str__(self):
        return f"{self.book.title} loaned to {self.borrower}"
