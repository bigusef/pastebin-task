from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Profile as UserProfile

# refrance to default user model
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    this serializer response for render and create new account
    """
    class Meta:
        model = User
        fields = 'id', 'username', 'password',
        read_only_fields = 'id',
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """
        override default create method to create new user account and fire account signal
        :return User account instance
        """
        password = validated_data.pop('password')
        instance = super().create(validated_data)
        instance.set_password(password)
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        override default to_representation method to return custome user account object
        :return User account object
        """
        return {
            'id': instance.pk,
            'username': instance.username,
            'token': instance.auth_token.key,
        }


class UserProfileSerializer(serializers.ModelSerializer):
    """
    this serializer respons on return and handel user profile
    """
    # custome serializer attribute
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
        """
        override default to_representation method to return custome user profile object
        :return User profile object
        """
        context = super().to_representation(instance)
        context.update({
            'gender': instance.get_gender_display(),
            'username': instance.user.username,
            'email': instance.user.email,
        })
        return context


class UserSerializer(serializers.ModelSerializer):
    """
    this serializer responed on handle user statistics views
    """

    # custome serializer attribute
    email = serializers.ReadOnlyField(source='user.email')
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        from authentication.models import Profile as UserProfile
        model = UserProfile
        fields = 'full_name', 'email', 'username',

    def to_representation(self, instance):
        """
        override default to_representation method to return custome user object
        :return User object
        """
        context = super().to_representation(instance)
        context.update({
            "total_pastes": instance.pastes_set.count(),
            "available_pastes": instance.pastes_set.available().count(),
            "unavailable_pastes": instance.pastes_set.unavailable().count()
        })
        return context
