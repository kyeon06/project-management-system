from django.contrib.auth.models import Group

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from kanbans.models import Column
from kanbans.serializers import ColumnCreateSerializer, ColumnDetailSerializer, ColumnSerializer
from teams.models import Team


# api/v1/kanbans/columns/
class ColumnAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ColumnCreateSerializer,
                         responses={
                             status.HTTP_201_CREATED : ColumnDetailSerializer
                         })
    def post(self, request):
        user = request.user
        column_name = request.data.get('name')
        team_name = request.data.get('team')
        
        try:
            team = Team.objects.get(name=team_name, leader=user)
        except Exception as e:
            return Response({"message" : "Column생성 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        order = Column.objects.filter(team=team).__len__() + 1
        
        data = {
            'name' : column_name,
            'order' : order,
            'team' : team.id
        }

        serializer = ColumnSerializer(data=data)
        if serializer.is_valid():
            saved_data = serializer.save()
            return Response(ColumnDetailSerializer(saved_data).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

