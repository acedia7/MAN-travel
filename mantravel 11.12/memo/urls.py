from django.urls import path
from .views import MemoListCreateView, MemoDetailView

urlpatterns = [
    path('memos/', MemoListCreateView.as_view(), name='memo-list-create'),  # 列表和创建
    path('memos/<int:pk>/', MemoDetailView.as_view(), name='memo-detail'),  # 详情、更新和删除
]