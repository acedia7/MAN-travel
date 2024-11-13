from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Memo
from .serializers import MemoSerializer
# Create your views here.


class MemoListCreateView(generics.ListCreateAPIView):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # 保存当前用户

class MemoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
    permission_classes = [IsAuthenticated]