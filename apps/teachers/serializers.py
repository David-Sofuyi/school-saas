from rest_framework import serializers
from .models import TeacherProfile
from apps.accounts.serializers import UserSerializer

class TeacherProfileSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source="user", read_only=True)
    class Meta:
        model = TeacherProfile
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]
