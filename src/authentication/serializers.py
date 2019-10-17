from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Profile as UserProfile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'username', 'password',
        read_only_fields = 'id',
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = super().create(validated_data)
        instance.set_password(password)
        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'username': instance.username,
            'token': instance.auth_token.key,
        }


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        exclude = 'id', 'user', 'created', 'updated',
        extra_kwargs = {
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'birth_date': {'write_only': True},
        }

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context.update({
            'gender': instance.get_gender_display(),
            'username': instance.user.username,
            'email': instance.user.email,
        })
        return context
