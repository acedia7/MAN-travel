from django.urls import path
from .views import BudgetView, BudgetDetail, ExpenseListCreate, ExpenseDetail

urlpatterns = [
    path('budgets/', BudgetView.as_view(), name='budget-list-create'),  # 列出和创建预算
    path('budgets/<int:pk>/', BudgetDetail.as_view(), name='budget-detail'),  # 获取、更新和删除预算
    path('expenses/', ExpenseListCreate.as_view(), name='expense-list-create'),  # 列出和创建费用
    path('expenses/<int:pk>/', ExpenseDetail.as_view(), name='expense-detail'),  # 获取、更新和删除费用
]