from rest_framework import serializers
from .models import Desk

class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = '__all__'