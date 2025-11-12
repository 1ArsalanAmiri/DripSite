from django_ratelimit.decorators import ratelimit
from rest_framework import generics
from ...models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from secrets import randbelow
from datetime import timedelta
from django_ratelimit.exceptions import Ratelimited
from .serializers import (
    RegisterUserSerializer,
    RequestOTPSerializer,
    VerifyOTPSerializer
)

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthViewSet(viewsets.ViewSet):
    """
    OTP Auth system with Redis rate limiting
    """

    def handle_exception(self, exc):
        if isinstance(exc, Ratelimited):
            return Response({"error": "Too many requests. Please try again later."},status=429)
        return super().handle_exception(exc)



    # ------------------------------
    @action(detail=False, methods=["post"])
    @ratelimit(key='ip', rate='5/m', block=True)
    def register(self, request):
        """Register user and send OTP"""
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        last_otp = EmailOTP.objects.filter(email=email).last()
        if last_otp and last_otp.is_blocked():
            remaining = int((last_otp.blocked_until - timezone.now()).total_seconds())
            return Response(
                {"error": f"Too many attempts. Try again in {remaining} seconds."},
                status=429
            )

        if last_otp and timezone.now() - last_otp.created_at < timedelta(minutes=2):
            return Response(
                {"error": "You can request OTP once every 2 minutes."},
                status=429
            )

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": serializer.validated_data["first_name"],
                "last_name": serializer.validated_data["last_name"],
                "gender": serializer.validated_data["gender"],
                "is_active": False
            }
        )

        code = "123456" if settings.DEBUG else f"{randbelow(1000000):06}"
        otp_entry = EmailOTP.objects.create(email=email, code=code)

        try:
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP code is: {code}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
        except Exception as e:
            otp_entry.delete()
            return Response({"error": f"Failed to send email: {str(e)}"}, status=500)

        return Response({"message": "OTP sent to your email"}, status=200)



    # ------------------------------
    @action(detail=False, methods=["post"])
    def verify_otp(self, request):
        """Verify OTP and activate user"""
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        otp = EmailOTP.objects.filter(email=email, is_used=False).last()
        if not otp:
            return Response({"error": "OTP not found"}, status=400)

        if otp.is_blocked():
            remaining = int((otp.blocked_until - timezone.now()).total_seconds())
            return Response(
                {"error": f"Too many wrong attempts. Try again in {remaining} seconds."},
                status=429
            )

        if otp.is_expired():
            return Response({"error": "OTP expired"}, status=400)

        if otp.code != code:
            otp.attempts += 1
            if otp.attempts >= 5:
                otp.blocked_until = timezone.now() + timedelta(minutes=15)
            otp.save()
            return Response({"error": "Invalid OTP"}, status=400)

        otp.is_used = True
        otp.save()

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found, please register first."}, status=404)

        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })


    # ------------------------------
    @action(detail=False, methods=["post"])
    @ratelimit(key='ip', rate='5/m', block=True)
    def request_otp(self, request):
        """Request a new OTP"""
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        last_otp = EmailOTP.objects.filter(email=email).last()
        if last_otp:
            if last_otp.is_blocked():
                remaining = int((last_otp.blocked_until - timezone.now()).total_seconds())
                return Response(
                    {"error": f"Too many attempts. Try again in {remaining} seconds."},
                    status=429
                )
            if timezone.now() - last_otp.created_at < timedelta(minutes=2):
                return Response(
                    {"error": "You can request OTP once every 2 minutes."},
                    status=429
                )

        code = "123456" if settings.DEBUG else f"{randbelow(1000000):06}"
        otp_entry = EmailOTP.objects.create(email=email, code=code)

        try:
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP code is: {code}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
        except Exception as e:
            otp_entry.delete()
            return Response({"error": f"Failed to send email: {str(e)}"}, status=500)

        return Response({"message": "OTP sent to your email"}, status=200)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter