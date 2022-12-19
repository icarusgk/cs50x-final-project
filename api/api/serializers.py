from rest_framework import serializers
from api.models import WorkSpace, Board, Card

class WorkSpaceSerializer(serializers.ModelSerializer):
  class Meta:
    model = WorkSpace
    fields = ['id', 'name']


class BoardSerializer(serializers.ModelSerializer):
  def get_fields(self):
    fields = super().get_fields()
    fields['cards'] = CardSerializer(many=True, required=False)
    return fields

  class Meta:
    depth = 1
    model = Board
    fields = ['id', 'name', 'cards']
  

class CardSerializer(serializers.ModelSerializer):
  class Meta:
    model = Card
    fields = ['id', 'name', 'description', 'board']
