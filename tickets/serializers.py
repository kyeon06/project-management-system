from rest_framework import serializers

from tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ('__all__')


class TicketDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    team = serializers.StringRelatedField()
    column = serializers.StringRelatedField()
    
    class Meta:
        model = Ticket
        fields = [
            'title',
            'order',
            'tag',
            'deadline',
            'workload',
            'column',
            'user',
            'team'
        ]


class TicketCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    tag = serializers.CharField()
    deadline = serializers.DateField()
    workload = serializers.FloatField()
    column = serializers.CharField()
    team = serializers.CharField()