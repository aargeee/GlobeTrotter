from rest_framework import serializers
from .models import GameScore

class GameScoreSerializer(serializers.Serializer):
    correct_answers = serializers.IntegerField()
    total_questions = serializers.IntegerField()
    percentage = serializers.IntegerField()

    def to_representation(self, instance):
        return {
            'correct_answers': instance.correct_answers,
            'total_questions': instance.total_questions,
            'percentage': instance.percentage,
        }
