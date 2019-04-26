from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from rest_framework.serializers import (
        EmailField,
    )


class UserSerializer(serializers.ModelSerializer):

    email = EmailField(label='Email Address')

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

    def validate(self, data):
        # email = data['email']
        # username = data['username']
        # user_qs = User.objects.filter(
        #   email=email) or User.objects.filter(username=username)
        # if user_qs.exists():
        #     raise ValidationError("This user has already registered.")
        return data