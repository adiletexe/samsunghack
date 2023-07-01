from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password1 = serializers.CharField(max_length=128, write_only=True)
    password2 = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password1']

        user = User.objects.create_user(username=username, password=password)
        return user

    class Meta():
        model = User
        fields = ['username', 'password1', 'password2']