from django.urls import path
from books import views

app_name = "books"

urlpatterns = [
    path("", views.BookListView.as_view(), name="list"),
    path("<int:pk>/", views.BookDetailView.as_view(), name="detail"),
    path("loan/", views.LoanBookApiView.as_view(), name="loan"),
    path("end-loan/<int:pk>/", views.EndBookLoanApiView.as_view(), name="end_loan"),
]