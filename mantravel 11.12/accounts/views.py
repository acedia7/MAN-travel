# views.py

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import generate_verification_code, verify_code, send_sms_code  # 引入验证码生成、验证和发送函数
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 正常的验证码生成逻辑
        try:
            code = generate_verification_code(phone)  # 生成验证码并存入缓存
            logger.info(f"Generated verification code for {phone}: {code}")

            # 发送验证码短信
            if not send_sms_code(phone, code):
                return Response({"error": "Failed to send SMS"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"message": "Verification code sent", "code": code}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Failed to generate or send verification code for {phone}: {e}")
            return Response({"error": "Failed to send verification code"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.utils import timezone

class LoginView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        code = request.data.get('code')

        if not phone or not code:
            return Response({"error": "Phone number and code are required"}, status=status.HTTP_400_BAD_REQUEST)

        # 验证用户输入的验证码
        if verify_code(phone, code):
            try:
                # 获取或创建用户
                user, created = User.objects.get_or_create(phone=phone)

                if created:
                    user.set_unusable_password()  # 如果自动注册用户，设一个不可用密码
                    user.save()

                # 更新 last_login 字段
                user.last_login = timezone.now()
                user.save()

                # 生成并返回 JWT token
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # 保存 access token 到数据库
                user.access_token = access_token
                user.save()

                return Response({
                    'refresh': str(refresh),
                    'access': access_token,
                }, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error during user registration or JWT token generation for {phone}: {e}")
                return Response({"error": "Error during registration or token generation"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.error(f"Invalid verification code for {phone}")
            return Response({"error": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)
