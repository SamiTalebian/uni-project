from rest_framework import serializers
from Auction.models import CustomUser, Contract
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class CustomUserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['pk', 'wallet_address', 'username',
                  'password', 'date_joined', 'role']
        extra_kwargs = {
            # Hide the password field in response
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
