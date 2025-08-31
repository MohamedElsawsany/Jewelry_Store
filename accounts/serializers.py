from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['role'] = user.role
        token['branch_id'] = user.branch.id
        token['branch_name'] = user.branch.name
        token['username'] = user.username
        
        return token

class UserSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'branch', 'branch_name', 'is_active', 'last_login']
        read_only_fields = ['id', 'last_login']