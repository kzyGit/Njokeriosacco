from rest_framework import serializers
from .models import User, Savings, Loans, LoanRepayment
from rest_framework.validators import UniqueValidator


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class RegistrationSerializer(serializers.ModelSerializer):
    query = User.objects.all()
    email = serializers.EmailField(validators=[
        UniqueValidator(queryset=query, message="Email already exists")
    ])

    id_number = serializers.IntegerField(validators=[
        UniqueValidator(
            queryset=query, message="Id number already registered")
    ])

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'middle_name', 'sur_name', 'email', 'id_number', 'image'
        ]

    def create(self, validated_data):
        validated_data['password'] = validated_data['email']
        return User.objects.create_user(**validated_data)


class savingsSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(required=True)
    user = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        serializer = RegistrationSerializer(
            instance=User.objects.get(user=obj.id))
        return serializer.data

    class Meta:
        model = Savings
        fields = ['id', 'amount', 'user', 'created_at', 'updated_at', 'mode']
        write_only_fields = ['amount']

    def create(self, validated_data):
        return Savings.objects.create(**validated_data)


class loansSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(required=True)
    user = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        serializer = RegistrationSerializer(
            instance=User.objects.get(loaner=obj.id))
        return serializer.data

    class Meta:
        model = Loans
        fields = ['id', 'amount', 'status', 'user', 'created_at', 'updated_at', 'repayment']
        write_only_fields = ['amount']

    def create(self, validated_data):
        return Loans.objects.create(**validated_data)


class LoanRepaymentsSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(required=True)

    class Meta:
        model = LoanRepayment
        fields = ['id', 'amount', 'created_at']

    def create(self, validated_data):
        return LoanRepayment.objects.create(**validated_data)
