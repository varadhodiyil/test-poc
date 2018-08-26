from rest_framework import serializers
from mishipay.core import models
from django.contrib.auth.hashers import check_password
from django.forms.widgets import PasswordInput

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(max_length=1000,
		style={'input_type': 'password'})


class UserRegistrationSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField()
	email = serializers.EmailField()
	password = serializers.CharField(max_length=1000,
		style={'input_type': 'password'})

	class Meta:
		model = models.Users
		fields = ('first_name','email','username','password')