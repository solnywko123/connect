from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=8, required=True, write_only=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password', 'password_confirm', 'last_name', 'first_name', 'avatar',
                  'username')

    def validate(self, attrs):
        password = attrs['password']
        password_confirm = attrs.pop('password_confirm')
        phone_number = attrs.get('phone_number').strip()

        if password != password_confirm:
            raise serializers.ValidationError(
                'Passwords didnt match!'
            )

        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError('Пароль не должен быть из одних цифр или букв')

        if phone_number[0] != '+':
            attrs['phone_number'] = '+' + phone_number

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
