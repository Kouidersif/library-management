from django.contrib import admin


@admin.action(description="End selected loans")
def end_loans(modeladmin, request, queryset):
    for loan in queryset:
        loan.is_returned = True
        loan.save()
        loan.book.is_available = True
        loan.book.save()
