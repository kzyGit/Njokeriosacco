from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class RegistrationSerializer(serializers.ModelSerializer):
    query = User.objects.all()
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=query,
                message="Email already exists"
            )
        ]
    )

    id_number = serializers.IntegerField(
        validators=[
            UniqueValidator(
                queryset=query,
                message="Id number already registered"
            )
        ]
    )

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'sur_name', 'email', 'id_number']

    def create(self, validated_data):
        validated_data['password']=validated_data['email']
        return User.objects.create_user(**validated_data)