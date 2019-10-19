from rest_framework import serializers

from authentication.serializers import UserProfileSerializer

from .models import Pastes


class PastesSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializer class related to snippet.Pastes model
    """

    # custom serializer attribute
    author = UserProfileSerializer(read_only=True)
    shared_user = UserProfileSerializer(source='allowed_user', read_only=True, many=True)
    expired = serializers.ReadOnlyField(source='is_expired')

    class Meta:
        model = Pastes
        exclude = 'allowed_user', 'expire_date', 'updated',
        extra_kwargs = {
            'url': {
                'lookup_field': "shortcode",
                "view_name": "snippet:pastes-detail",
            }
        }

    def create(self, validated_data):
        """
        override create method and make sure is user is authenticated the created pastes will attaced to him
        """
        auth_user = self.context.get('auth_user')
        if auth_user.is_authenticated:
            validated_data.update({
                'author': auth_user.profile
            })
        return super().create(validated_data)

    def validate(self, data):
        """
        overrider validate method to make sure that guest user will alwes create public pastes
        """
        auth_user = self.context.get('auth_user')
        if not auth_user.is_authenticated and data['privacy'] != Pastes.PUBLIC:
            raise serializers.ValidationError("Only allowed privacy is Public")
        return data

    def to_representation(self, instance):
        """
        handel representation for innstance and make sure 'allwed_suer' not shown only if pastes is sheard
        """
        context = super().to_representation(instance)
        if instance.privacy != Pastes.SHARED:
            del context['shared_user']
        context.update({
            'expiration': instance.get_expiration_display(),
            'privacy': instance.get_privacy_display(),
        })
        return context


class AllwedUserSerializer(serializers.ModelSerializer):
    """
    serializer class responsbile on handel allowed_user relation bettwen pastes owner and other users
    """

    # custome serilizer attribute
    shared_user = UserProfileSerializer(source='allowed_user', read_only=True, many=True)

    class Meta:
        model = Pastes
        fields = 'allowed_user', 'shared_user',
        extra_kwargs = {
            'allowed_user': {'write_only': True},
        }

    def update(self, instance, validated_data):
        """
        override update method to make sure current pastes is shared before updated the relation
        """
        if instance.privacy == Pastes.SHARED:
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError("Can't select shared user unless you select your Privacy as Shared")
