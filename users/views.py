from django.contrib.auth.models import Group

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from users.models import User

from users.serializers import SignupOutputSerializer, SignupSerializer


# api/v1/users/signup/
class SignupView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=SignupSerializer,
        responses = {
            status.HTTP_201_CREATED : SignupOutputSerializer
        }
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()

            data = {
                "username" : user.username,
                "email" : user.email,
                "message" : "회원가입이 완료되었습니다."
            }

            return Response(data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api/v1/users/invite/
class UserInviteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.invite_message is None:
            return Response({"message" : "초대받은 기록이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        team_name = user.invite_message.split("|")[0].split(":")[1]
        leader = user.invite_message.split("|")[1].split(":")[1]

        return Response({"message" : f"{leader}님이 {team_name}에 초대하셨습니다."}, status=status.HTTP_200_OK)


# api/v1/users/invite/accept/
class UserInviteAcceptAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        유저가 초대 받은 초대장을 수락할 경우 실행
        """
        user = request.user
        invite_message = user.invite_message

        team_name = invite_message.split("|")[0].split(":")[1]

        # team 그룹 가져오기
        team_group = Group.objects.get(name=team_name.strip())
        user.groups.add(team_group)

        # user invite_message 삭제
        user.invite_message = None
        user.save()

        data = {
            "message" : f"{team_name} 초대를 수락하셨습니다."
        }

        return Response(data, status=status.HTTP_200_OK)
    

# api/v1/users/invite/refuse/
class UserInviteRefuseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        invite_message = user.invite_message

        team_name = invite_message.split("|")[0].split(":")[1]

        user.invite_message = None
        user.save()

        data = {
            "messsage" : f"{team_name} 초대를 거절하셨습니다."
        }

        return Response(data, status=status.HTTP_200_OK)