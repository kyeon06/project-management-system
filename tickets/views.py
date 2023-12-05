from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from kanbans.models import Column
from teams.models import Team
from tickets.models import Ticket
from tickets.serializers import TicketCreateSerializer, TicketDetailSerializer, TicketSerializer

from users.models import User


# api/v1/tickets/
class TicketAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=TicketCreateSerializer,
                         responses={
                             status.HTTP_201_CREATED : TicketDetailSerializer
                         })
    def post(self, request):
        user = request.user
        title = request.data.get('title')
        tag = request.data.get('tag')
        deadline = request.data.get('deadline')
        workload = request.data.get('workload')
        column_name = request.data.get('column')
        team_name = request.data.get('team')

        try:
            team = Team.objects.get(name=team_name)
        except Exception as e:
            return Response({"message" : f"{team_name}이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        group_users = User.objects.filter(groups__name=team_name)
        if user not in group_users:
            return Response({"message" : "Ticket 생성 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            column = Column.objects.get(team=team, name=column_name)
        except Exception as e:
            return Response({"message" : f"{column_name}을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        order = Ticket.objects.filter(team=team, column=column).__len__() + 1
        
        data = {
            "user" : user.id,
            "title" : title,
            "tag" : tag,
            "order" : order,
            "deadline" : deadline,
            "workload" : workload,
            "column" : column.id,
            "team" : team.id
        }

        serializer = TicketSerializer(data=data)
        if serializer.is_valid():
            saved_data = serializer.save()
            return Response(TicketDetailSerializer(saved_data).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)