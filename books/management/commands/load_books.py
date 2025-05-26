from books.models import Book, Author
from django.core.management.base import BaseCommand
import random
import uuid
class Command(BaseCommand):
    help = 'Create Dummy Data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for i in range(1, 11):
            author = Author.objects.filter(first_name=f"Author {random.randint(1, 5)}").first()
            if not author:
                author = Author.objects.create(
                    first_name=f"Author {i}",
                    last_name=f"Last Name {i}",
                )
            books = Book.objects.create(
                title=f"Book {i}",
                author=author,
                isbn=f"{str(uuid.uuid4())[:13]}",
                page_count=i * 50,
                is_available=True,
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully created Dummy Data'))
        
