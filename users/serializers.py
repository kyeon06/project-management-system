from rest_framework import serializers

from users.models import User


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]
    
    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("유저가 존재합니다. 다른 계정명을 사용해주세요.")
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("해당 이메일이 존재합니다. 다른 이메일을 사용해주세요.")
        
        user = User.objects.create_user(username=username, email=email, password=password)

        return user


class SignupOutputSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    message = serializers.CharField()