from django.db import models
import uuid
import random
from django.db.models import Count

# Create your models here.
class Destination(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.city}, {self.country}"
    
class DestinationInfo(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    info = models.TextField()
    is_active = models.BooleanField(default=True)

    class InfoType(models.TextChoices):
        CLUE = 'CLUE', 'Clue'
        FUN_FACT = 'FUN_FACT', 'Fun Fact'
        TRIVIA = 'TRIVIA', 'Trivia'
    
    type = models.CharField(max_length=10, choices=InfoType.choices)

    def __str__(self):
        return f"{self.destination} at {self.info}"

    class Meta:
        indexes = [
            models.Index(fields=['destination', 'type']),
        ]

class GameScore:
    def __init__(self, correct_answers, total_questions):
        self.correct_answers = correct_answers
        self.total_questions = total_questions
        self.percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0

    def __str__(self):
        return f"Score: {self.percentage:.2f}% ({self.correct_answers}/{self.total_questions})"

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.player} at {self.id}"

    def get_score(self) -> GameScore:
        total_questions = Question.objects.filter(game=self).count()
        correct_answers = Question.objects.filter(game=self, is_answered_correctly=True).count()
        return GameScore(correct_answers, total_questions)
    
    @classmethod
    def get_player_high_score(cls, player):
        games = cls.objects.filter(player=player)
        high_score = None
        for game in games:
            score = game.get_score()
            high_score = score if high_score is None or score.correct_answers > high_score.correct_answers else high_score
        return high_score
    
    @classmethod
    def get_global_high_score(cls):
        highest_score_game = (
            Question.objects.filter(is_answered_correctly=True)
            .values('game')
            .annotate(correct_count=Count('id'))
            .order_by('-correct_count')
            .first()
        )

        if highest_score_game:
            game_id = highest_score_game['game']
            game = Game.objects.get(id=game_id)
            return game
        return GameScore(0, 0)

    class Meta:
        indexes = [
            models.Index(fields=['player', 'is_active']),
        ]

class Question(models.Model):
    clues = models.ManyToManyField(DestinationInfo, limit_choices_to={'type': 'CLUE'})
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_answered_correctly = models.BooleanField(default=False)

    def __str__(self):
        return f"Question for {self.destination} in game {self.game}"

    @classmethod
    def new_question(cls, game: Game):
        answered_destinations = Question.objects.filter(game=game).values_list('destination', flat=True)
        destinations = Destination.objects.exclude(id__in=answered_destinations)
        
        if not destinations.exists():
            game.is_active = False
            game.save()
            return None
        destination = random.choice(destinations)
        question = cls.objects.create(game=game, destination=destination)
        clues = list(DestinationInfo.objects.filter(destination=destination, type=DestinationInfo.InfoType.CLUE))
        selected_clues = random.sample(clues, min(len(clues), 2))
        question.clues.set(selected_clues)
        question.save()
        return question

    class Meta:
        indexes = [
            models.Index(fields=['game', 'is_answered_correctly']),
        ]
