from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Desk, Worker

class  UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        """
        Validate that passwords match.
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Hasła muszą być takie same")
        return data

    def create(self, validated_data):
        """
        Create a new user with the validated data.
        """
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
        except Exception as e:
            raise serializers.ValidationError(f"Error creating user: {str(e)}")
        return user

