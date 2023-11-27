from rest_framework import serializers

from teams.models import Team


class TeamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Team
        fields = ('__all__')


class TeamDetailSerializer(serializers.ModelSerializer):
    leader = serializers.StringRelatedField()

    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'leader'
        ]


class TeamInviteSerializer(serializers.Serializer):
    invite_user = serializers.CharField()