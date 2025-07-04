from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import ExpenseIncome

# Serializer for displaying user info
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Serializer for registering new users
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # for password confirmation

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn’t match."})
        return attrs

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class ExpenseSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = ExpenseIncome
        fields = [
            'id',
            'title',
            'description',
            'amount',
            'transaction_type',
            'tax',
            'tax_type',
            'total',
            'created_at',
            'updated_at',
        ]

    def get_total(self, obj):
        if obj.tax_type == 'flat':
            return obj.amount + obj.tax
        return obj.amount + (obj.amount * obj.tax / 100)
        
class ExpenseListSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = ExpenseIncome
        fields = ['id', 'title', 'amount', 'transaction_type', 'total', 'created_at']

    def get_total(self, obj):
        if obj.tax_type == 'flat':
            return obj.amount + obj.tax
        return obj.amount + (obj.amount * obj.tax / 100)
