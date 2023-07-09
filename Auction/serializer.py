from rest_framework import serializers
from Auction.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['pk','wallet_address','username','password','date_joined','role']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()