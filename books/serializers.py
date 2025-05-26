from rest_framework import serializers
from books.models import Book, Loan, Author
from accounts.serializers import UserSerializer

class BookCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    class Meta:
        model = Book
        fields = ["title", "author", "isbn", "page_count", "is_available"]
        
    


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["first_name", "last_name", "id"]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    class Meta:
        model = Book
        fields = ["title", "author", "isbn", "page_count", "is_available", "id"]
        
        



class LoanSerializer(serializers.ModelSerializer):
    borrower = UserSerializer()
    book = BookSerializer()
    class Meta:
        model = Loan
        fields = ["book", "borrower", "loan_date", "return_date", "is_returned", "id"]
        



class LoanBookSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(LoanBookSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get("request")
        self.user = self.request.user if self.request else None
    
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    class Meta:
        model = Loan
        fields = ["book", "return_date"]
        
    def validate(self, attrs):
        attrs = super().validate(attrs)
        book = attrs.get("book")
        # if already loaned
        if Loan.objects.filter(book=book, borrower=self.user, is_returned=False).exists():
            raise serializers.ValidationError({"book": "You already have a loan for this book."})
        if not book.is_available:
            raise serializers.ValidationError({"book": "Book is not available."})
        
        
        return attrs
        
    def create(self, validated_data):
        user = self.user
        validated_data["borrower"] = user
        instance = super().create(validated_data)
        instance.book.is_available = False
        instance.book.save()
        return instance
    