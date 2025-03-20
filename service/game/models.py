from django.db import models
import uuid
import random
from django.db.models import Count


class Difficulty(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
# Create your models here.
class Destination(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    difficulty = models.ForeignKey('Difficulty', on_delete=models.CASCADE)

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

class LeaderBoardEntry:
    def __init__(self, player, score):
        self.player = player
        self.score = score

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.player} at {self.id}"

    def get_score(self) -> GameScore:
        total_questions = Question.objects.filter(game=self).count()
        correct_answers = Question.objects.filter(game=self, is_answered_correctly=True).count()
        return GameScore(correct_answers, total_questions)
    
    def save(self, force_insert = ..., force_update = ..., using = ..., update_fields = ...):
        return super().save(force_insert, force_update, using, update_fields)
    
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
    
    @classmethod
    def get_leaderboard(cls, difficulty, page, per_page):
        highest_score_games = (
            Question.objects.filter(is_answered_correctly=True, game__difficulty=difficulty)
            .values('game')
            .annotate(correct_count=Count('id'))
            .order_by('-correct_count')
        )

        high_scores = []
        players = set()
        for high_score_game in highest_score_games:
            game_id = high_score_game['game']
            game = Game.objects.get(id=game_id)
            if game.player in players:
                continue
            high_scores += [LeaderBoardEntry(player=game.player, score=game.get_score())]
            players.add(game.player)
        return high_scores[page: page * per_page + per_page]

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
        destinations = Destination.objects.exclude(id__in=answered_destinations).filter(difficulty=game.difficulty)
        
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

class PlayerScore(models.Model):
    player = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    score = models.IntegerField()
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.player} scored {self.score} in {self.game}"

    class Meta:
        indexes = [
            models.Index(fields=['player', 'game']),
        ]

class Player(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    high_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}"

    @classmethod
    def get_or_create_player(cls, user):
        player, created = cls.objects.get_or_create(user=user)
        return player

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]