from rest_framework import status, generics, permissions
from rest_framework.response import Response
from books.serializers import BookSerializer, LoanSerializer, LoanBookSerializer
from books.models import Book, Loan, Author
from django.utils import timezone
from drf_yasg.inspectors import SwaggerAutoSchema


class BooksSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        return ["Books API"]


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    swagger_schema = BooksSchema


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    swagger_schema = BooksSchema




class LoanBookApiView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanBookSerializer
    permission_classes = [permissions.IsAuthenticated]
    swagger_schema = BooksSchema



class EndBookLoanApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    swagger_schema = BooksSchema
    def post(self, request, pk):
        loan = Loan.objects.filter(pk=pk).first()
        if not loan:
            return Response(
                {"detail": "Loan not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if loan.is_returned:
            return Response(
                {"detail": "Loan already returned."}, status=status.HTTP_400_BAD_REQUEST
            )
        loan.is_returned = True
        loan.return_date = timezone.now()
        loan.save()
        # set book as available
        loan.book.is_available = True
        loan.book.save()
        return Response(
            {"detail": "Loan ended successfully."}, status=status.HTTP_200_OK
        )


