from django.contrib.auth import get_user_model
from django.conf import settings

from users import serializers
from users import models
from users.forms import UserRegisterForm
from users.utils import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UserCreate(APIView):
    """
    Creates a new user.
    """

    def post(self, request):
        """
        Creates a new user.
        """
        form = UserRegisterForm(request.data)
        if form.is_valid():
            # Verification mail Content
            from_mail = settings.EMAIL_HOST_USER
            to_mail = form.cleaned_data["email"]
            user_name = form.cleaned_data["name"]
            verify_link = "link"
            # create user
            form.save()
            # send verification email
            send_verify_email(
                to_mail=to_mail, from_mail=from_mail, verify_link=verify_link
            )
            return Response({"detail": "User Registered. Please check your email"})
        return Response(form.errors, status=400)


class EMailVerifyView(APIView):
    def get(self, request, token):
        if (
            get_user_model()
            .objects.filter(email_verified_hash=token, is_active=False)
            .exists()
        ):
            user = get_user_model().objects.get(email_verified_hash=token)
            user.is_active = True
            user.save()
            return Response({"detail": "Email verified successfully"})
        else:
            return Response({"error": "Invalid request"}, status=400)


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        email = request.user.email
        user = models.User.objects.get(email=email)
        serializer = serializers.UserSerializer(user)
        result = serializer.data
        print(serializer.data)
        return Response(result)


class ResetPasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        # check old password
        email = request.user.email
        user = models.User.objects.get(email=email)

        if not user.check_password(request.data["old_password"]):
            return Response({"detail": "Old password is incorrect"}, status=400)
        # change new password
        user.set_password(request.data["new_password"])
        user.save()
        return Response({"detail": "password changed"})


class ChangeName(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        email = request.user.email
        user = models.User.objects.get(email=email)
        user.name = request.data["name"]
        user.save()
        return Response({"detail": "name changed"})


class AvatarChange(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        email = request.user.email
        user = models.User.objects.get(email=email)
        prev_image = user.avatar
        new_avatar = selectImage()
        while new_avatar == prev_image:
            new_avatar = selectImage()

        user.avatar = new_avatar
        user.save()
        return Response({"detail": "avatar changed", "new_avatar": new_avatar})


class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data["email"]
        if email is None:
            return Response({"detail": "email not provided"}, status=400)
        if get_user_model().objects.filter(email=email).exists():
            from_mail = settings.EMAIL_HOST_USER
            to_mail = email

            send_reset_email(to_mail=to_mail, from_mail=from_mail)
            return Response({"detail": "Email sent"})
        else:
            return Response({"error": "Email not found"}, status=400)


class NewPasswordView(APIView):
    def post(self, request, token):
        if get_user_model().objects.filter(reset_password_hash=token).exists():
            user = get_user_model().objects.get(reset_password_hash=token)
            user.set_password(request.data["new_password"])
            user.save()
            return Response({"detail": "Password changed"})
        else:
            return Response({"error": "Invalid request"}, status=400)
