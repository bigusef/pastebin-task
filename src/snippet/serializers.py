from rest_framework import serializers

from authentication.serializers import UserProfileSerializer
from .models import Pastes


class PastesSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    shared_user = UserProfileSerializer(read_only=True, many=True)
    expired = serializers.ReadOnlyField(source='is_expired')

    class Meta:
        model = Pastes
        exclude = 'id', 'updated', 'expire_date',
        extra_kwargs = {
            'allowed_user': {'write_only': True},
        }

    def create(self, validated_data):
        auth_user = self.context.get('auth_user')
        if auth_user.is_authenticated:
            validated_data.update({
                'author': auth_user.profile
            })
        return super().create(validated_data)

    def validate(self, data):
        auth_user = self.context.get('auth_user')
        if not auth_user.is_authenticated and data['privacy'] != Pastes.PUBLIC:
            raise serializers.ValidationError("Only allowed privacy is Public")
        if data['privacy'] != Pastes.SHARED and data['allowed_user']:
            raise serializers.ValidationError("Can't select shared user unless you select your Privacy as Shared")
        return data

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context.update({
            'expiration': instance.get_expiration_display(),
            'privacy': instance.get_privacy_display(),
            'shortcode': instance.get_absolute_url(),
        })
        return context
