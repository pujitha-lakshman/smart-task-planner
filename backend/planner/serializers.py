from rest_framework import serializers
from .models import CompletedTask

class CompletedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedTask
        fields = '__all__'
