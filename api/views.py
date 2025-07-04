from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import ExpenseIncome as Expense
from .serializers import ExpenseSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncWeek 

from calendar import monthrange

#
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # Superuser can see all expenses
            return Expense.objects.all()
        # Normal users see only their own records
        return Expense.objects.filter(user=user)

    def perform_create(self, serializer):
        # Save the user on create
        serializer.save(user=self.request.user)

    def get_object(self):
        obj = super().get_object()
        # Only allow owners or superusers to access the object
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to access this record.")
        return obj



class ExpenseAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        expenses = Expense.objects.filter(user=user)
        if start_date and end_date:
            expenses = expenses.filter(date__range=[start_date, end_date])

        total = expenses.aggregate(total=Sum("amount"))["total"] or 0

        category_data = (
            expenses
            .values("category")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )
        category_summary = {item["category"]: float(item["total"]) for item in category_data}

        daily_data = (
            expenses
            .annotate(day=TruncDay("date"))
            .values("day")
            .annotate(total=Sum("amount"))
            .order_by("day")
        )
        daily_summary = {str(item["day"]): {
            "total": float(item["total"]),
            "average": float(item["total"])
            }
            for item in daily_data
        }

        monthly_data = (
            expenses
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )
        monthly_summary = {
            str(item["month"]): {
            "total": float(item["total"]),
            "average": round(
            float(item["total"]) / monthrange(item["month"].year, item["month"].month)[1], 2
            )}
            for item in monthly_data
        }
        
        weekly_data = (
            expenses
            .annotate(week=TruncWeek("date"))
            .values("week")
            .annotate(total=Sum("amount"))
            .order_by("week")
        )
        weekly_summary = {
            str(item["week"]): {
            "total": float(item["total"]),
            "average": round(float(item["total"]) / 7, 2)
            }
            for item in weekly_data
        }


        return Response({
            "total_expenses": float(total),
            "category_breakdown": category_summary,
            "daily_trends": daily_summary,
            "weekly_trends": weekly_summary,
            "monthly_trends": monthly_summary,
        })