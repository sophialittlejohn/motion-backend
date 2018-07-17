from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.serializers.users import UserSerializer, UserPrivateInfoSerializer

User = get_user_model()


class ListUsersView(APIView):
    def get(self, request):
        # print all users either with or without search params
        search = request.query_params.get('search')
        if search:
            users = User.objects.filter(username__contains=search)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserByIdView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404
        serializer = UserSerializer(user)
        return Response(serializer.data)


class GetUpdateUserProfile(APIView):
    def get(self, request):
        # gets my user profile including private information
        user = request.user
        serializer = UserPrivateInfoSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        # update user profile private info
        user = request.user
        serializer = UserPrivateInfoSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
