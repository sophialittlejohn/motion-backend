from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from project.api.serializers.password_reset import PasswordResetSerializer, PasswordResetValidationSerializer
from project.api.serializers.registration import RegistrationSerializer, RegistrationValidationSerializer


class RegistrationView(GenericAPIView):
    # follow a user
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.register_user(serializer.validated_data.get('email'))
        return Response({
            'email': new_user.email
        })


class RegistrationValidationView(GenericAPIView):
    # follow a user
    permission_classes = [AllowAny]
    serializer_class = RegistrationValidationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(serializer.validated_data)
        return Response(self.get_serializer(user).data)


class PasswordResetView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.recover_user(serializer.validated_data.get('email'))
        return Response({
            'email': user.email
        })


class PasswordResetValidate(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetValidationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(serializer.validated_data)
        return Response(self.get_serializer(user).data)
