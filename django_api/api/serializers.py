from rest_framework import serializers
from .models import ApiPost

class ApiPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiPost
        fields = '__all__'