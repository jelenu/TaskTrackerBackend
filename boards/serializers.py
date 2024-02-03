# tasks/serializers.py
from rest_framework import serializers
from .models import Board, List, Card

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'title', 'description', 'order']

class ListSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = ['id', 'name', 'order', 'cards']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['cards'] = sorted(representation['cards'], key=lambda x: x['order'])
        return representation

class BoardSerializer(serializers.ModelSerializer):
    lists = ListSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'name', 'lists']
