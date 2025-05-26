from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from books.models import Book, Author, Loan
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class BooksTests(APITestCase):
    def setUp(self):
        """Set up test data"""
        # Create test client
        self.client = APIClient()
        
        # Create a test user
        self.user = User.objects.create(
            email='testuser@example.com',
            first_name='Test',
            last_name='User'
        )
        
        # Create test author
        self.author = Author.objects.create(
            first_name='John',
            last_name='Doe'
        )
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Test Book 1',
            author=self.author,
            isbn='1234567890123',
            page_count=200,
            is_available=True
        )
        
        self.book2 = Book.objects.create(
            title='Test Book 2',
            author=self.author,
            isbn='1234567890124',
            page_count=300,
            is_available=False
        )
        
        # Set up URLs
        self.book_list_url = reverse('books:list')
        self.book_detail_url = reverse('books:detail', kwargs={'pk': self.book1.pk})
        self.loan_book_url = reverse('books:loan')
        
        # Authentication
        self.client.force_authenticate(user=self.user)

    def test_list_books(self):
        """Test listing all books"""
        response = self.client.get(self.book_list_url)
        results = response.json()["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 2)

    def test_filter_available_books(self):
        """Test filtering books by availability"""
        response = self.client.get(f"{self.book_list_url}?is_available=true")
        results = response.json()["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['isbn'], '1234567890123')

    def test_search_books(self):
        """Test searching books by title"""
        response = self.client.get(f"{self.book_list_url}?search=Book 1")
        results = response.json()["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Test Book 1')

    def test_get_book_detail(self):
        """Test retrieving a specific book"""
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], 'Test Book 1')
        self.assertEqual(response.json()['isbn'], '1234567890123')

    def test_loan_book(self):
        """Test creating a book loan"""
        data = {
            'book': self.book1.pk,
            'return_date': (timezone.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        }
        response = self.client.post(self.loan_book_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify book is no longer available
        self.book1.refresh_from_db()
        self.assertFalse(self.book1.is_available)

    def test_loan_unavailable_book(self):
        """Test attempting to loan an unavailable book"""
        data = {
            'book': self.book2.pk,
            'return_date': (timezone.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        }
        response = self.client.post(self.loan_book_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_end_book_loan(self):
        """Test ending a book loan"""
        # Create a loan first
        loan = Loan.objects.create(
            book=self.book1,
            borrower=self.user,
            return_date=timezone.now() + timedelta(days=14)
        )
        self.book1.is_available = False
        self.book1.save()
        
        # End the loan
        end_loan_url = reverse('books:end_loan', kwargs={'pk': loan.pk})
        response = self.client.post(end_loan_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify book is available again
        self.book1.refresh_from_db()
        self.assertTrue(self.book1.is_available)
        
        # Verify loan is marked as returned
        loan.refresh_from_db()
        self.assertTrue(loan.is_returned)

    def test_end_nonexistent_loan(self):
        """Test ending a non-existent loan"""
        end_loan_url = reverse('books:end_loan', kwargs={'pk': 99999})
        response = self.client.post(end_loan_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

