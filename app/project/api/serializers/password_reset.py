from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from rest_framework import serializers

from project.feed.models import Profile

User = get_user_model()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label='E-Mail addresss'
    )

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')

    def send_new_code(self, email, code):
        message = EmailMessage(
            subject='Social feed password reset',
            body=f'This is your new code --> {code}',
            to=[email],
        )
        message.send()

    def recover_user(self, user):
        user.user_profile.generate_new_code()
        self.send_new_code(
            email=user.email,
            code=user.user_profile.registration_code,
        )
        return user


class PasswordResetValidationSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        label='validation code',
        write_only=True,
    )
    password = serializers.CharField(
        label='password',
        write_only=True,
    )
    password_repeat = serializers.CharField(
        label='password_repeat',
        write_only=True,
    )

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_repeat'):
            raise serializers.ValidationError({
                "password": "Passwords don't match"
            })
        return attrs

    def validate_code(self, value):
        try:
            return User.objects.get(user_profile__registration_code=value, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Wrong validation code or already validated!'
            )

    def save(self, validated_data):
        user = validated_data.get('code')
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    class Meta:
        model = Profile
        fields = ['id', 'code', 'password', 'password_repeat']
        read_only_fields = ['id']

    def to_representation(self, user):
        data = super().to_representation(user)
        return {
            **data,
            'username': user.username,
            # takes the likes from each post and creates a list and then sums up the list for total likes
            'fame_index': sum([p.likes.count() for p in user.posts.all()]),
            'followers_count': user.followers.count(),
        }
