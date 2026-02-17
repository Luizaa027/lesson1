from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
import random
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import PasswordResetCode


from apps.users.models import User
from apps.users.serializers import RegisterSerializers, UserProfileSerializers

class RegisterAPI(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers

class ProfileAPI(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializers
    permission_classes = [IsAuthenticated,]



class SendResetCodeAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        code = str(random.randint(100000, 999999))

        PasswordResetCode.objects.create(user=user, code=code)

        send_mail(
            subject="Your password reset code",
            message=f"Your code: {code}",
            from_email="your_email@gmail.com",
            recipient_list=[email],
        )

        return Response({"message": "Code sent to email"})

class VerifyCodeAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        try:
            user = User.objects.get(email=email)
            reset_code = PasswordResetCode.objects.filter(user=user).last()
        except:
            return Response({"error": "Invalid data"}, status=400)

        if reset_code.code != code:
            return Response({"error": "Invalid code"}, status=400)

        return Response({"message": "Code verified"})

class ResetPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        new_password = request.data.get("new_password")

        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password changed successfully"})
