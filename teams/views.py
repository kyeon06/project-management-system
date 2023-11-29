from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from teams.models import Team

from teams.serializers import TeamDetailSerializer, TeamInviteSerializer, TeamSerializer
from users.models import User
from users.serializers import UserSerializer


# api/v1/teams/
class TeamCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(request_body=TeamSerializer,
                         responses={
                             status.HTTP_201_CREATED : TeamDetailSerializer
                         })
    def post(self, request):
        name = request.data.get('name', None)
        data = request.data

        if name is None:
            return Response({"message" : "팀명을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        is_exists = Team.objects.filter(name=name).exists()
        if is_exists:
            return Response({"message" : "이미 존재하는 팀명입니다. 다시 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        data['leader'] = request.user.id

        serializer = TeamSerializer(data=data)
        if serializer.is_valid():
            saved_data = serializer.save()

            return Response(TeamDetailSerializer(saved_data).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors(), status=status.HTTP_400_BAD_REQUEST)


class TeamInviteAPIView(APIView):
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(request_body=TeamInviteSerializer,
                         responses={
                             status.HTTP_200_OK : UserSerializer
                         })
    def post(self, request, team_id):
        user = request.user

        try:
            team = Team.objects.get(id=team_id)
        except Exception as e:
            return Response({"message" : "해당 팀 정보가 존재하지 않습니다"}, status=status.HTTP_404_NOT_FOUND)
        
        if user.username != team.leader.username:
            return Response({"message" : "초대 권한이 없습니다. 초대는 팀장만 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        invite_user = request.data.get("invite_user")
        try:
            invite_user_instance = User.objects.get(username=invite_user)
        except Exception as e:
            return Response({"message" : "해당 멤버가 존재하지 않습니다"}, status=status.HTTP_404_NOT_FOUND)
        
        if invite_user_instance.invite_message is not None:
            return Response({"message" : "이미 초대된 유저입니다."}, status=status.HTTP_400_BAD_REQUEST)
        

        data = {
            "invite_message" : f"team:{team.name} | from:{team.leader.username}"
        }

        serializer = UserSerializer(invite_user_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)