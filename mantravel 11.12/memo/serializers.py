from rest_framework import serializers
from .models import Memo

class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ['id',  'name', 'note', 'status', 'created_at']