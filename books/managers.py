

from django.db import models
from django.utils import timezone


class BooksQuerysetManager(models.QuerySet):
    """Queryset manager for Book model with additional filters."""
    def available(self):
        return self.filter(is_available=True)
    
    def borrowed(self):
        return self.filter(is_available=False)




class LoansQuerysetManager(models.QuerySet):
    """Queryset manager for Loan model with additional filters."""
    def active(self):
        return self.filter(is_returned=False)
    
    def returned(self):
        return self.filter(is_returned=True)
    
    def overdue(self):
        return self.filter(return_date__lt=timezone.now())