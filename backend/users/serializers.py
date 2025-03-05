from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only = True)
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password and Confirm password do not match")
    
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "This email already exists"})

        return data 
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
    
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username = username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('User is deactivated')
            else:
                raise serializers.ValidationError('Invalid Credentials')
        else:
            raise serializers.ValidationError('Username and password must be provided')
        
        return data
    

class recoverEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        if not get_user_model().objects.filter(email = data['email']).exists():
            raise serializers.ValidationError({'email': "There is no user registered with this email address"})
        
        return data