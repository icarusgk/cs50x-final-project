from rest_framework import serializers
from api.models import WorkSpace

class WorkSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSpace
        fields = ['id', 'name']