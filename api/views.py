from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import check_password

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status, APIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.authtoken.models import Token

from .decorators import validate_request_data
from .serializers import *
from .utils import generate_qr
from .models import Songs


class CreateQRView(generics.CreateAPIView):
    """
    POST create/
    """
    permission_classes = (permissions.AllowAny,)
    queryset = ''
    serializer_class = QRSerializer
    throttle_classes = [AnonRateThrottle]

    @validate_request_data
    def post(self, request, *args, **kwargs):
        text = request.data['text']
        output = generate_qr(text)
        result = QRSerializer(output).data
        return Response(
            data=result,
            status=status.HTTP_201_CREATED
        )


class SongsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET songs/:id/
    PUT songs/:id/
    DELETE songs/:id/
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    throttle_class = [UserRateThrottle]

    def get(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            return Response(SongsSerializer(a_song).data)
        except Songs.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            serializer = SongsSerializer()
            updated_song = serializer.update(a_song, request.data)
            return Response(SongsSerializer(updated_song).data)
        except Songs.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            a_song.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Songs.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """

    # This permission class will over ride the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    throttle_classes = ''
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        none_check = username or password is None
        empty_check = username or password is ''
        if (none_check or empty_check) is True:
            return Response(data={"message": "Username and password required"},
                            status=status.HTTP_401_UNAUTHORIZED)
        get_password = User.objects.get(username__exact=username).password
        password_check = check_password(password, get_password)
        if password_check is True:
            user = authenticate(username=username, password=password)
            if user is not None:
                # login saves the user’s ID in the session,
                # using Django’s session framework.
                login(request, user)
                token = Token.objects.get_or_create(user=user)
                return Response(
                    data={"token": token[0].key},
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                data={"message": "Username or password incorrect"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        # simply delete the session information
        request.session.flush()
        return Response(
            data={"message": "You are logged out."},
            status=status.HTTP_200_OK)


class RegisterUsers(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    throttle_classes = ''

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            new_user = User.objects.create_user(
                username=username, password=password, email=email
            )
        except IntegrityError:
            return Response(
                data={"message": "Username and Email should be unique"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data={"message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )

