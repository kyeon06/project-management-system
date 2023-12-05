from rest_framework import serializers

from kanbans.models import Column

class ColumnSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Column
        fields = [
            'name',
            'order',
            'team'
        ]


class ColumnDetailSerializer(serializers.ModelSerializer):
    team = serializers.StringRelatedField()
    
    class Meta:
        model = Column
        fields = [
            'name',
            'order',
            'team'
        ]
 


class ColumnCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    team = serializers.CharField()