from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from teams.models import Team

from teams.serializers import TeamDetailSerializer, TeamSerializer


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
