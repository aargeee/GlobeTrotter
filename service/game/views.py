from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Game, Question, Destination, DestinationInfo
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import uuid
from .serializers import GameScoreSerializer

from rest_framework import serializers

class UnregisteredUserTokenView(APIView):
    """
    API view to generate tokens for unregistered users.
    """
    permission_classes = []
    def post(self, request, *args, **kwargs):
        """
        Generates a new unregistered user ID and returns a refresh and access token.
        """
        unregistered_user_id = str(uuid.uuid4())
        unregistered_user = User.objects.create(username=unregistered_user_id)
        refresh = RefreshToken.for_user(unregistered_user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class UnregisteredUserTokenRefreshView(APIView):
    """
    API view to refresh tokens for unregistered users.
    """
    permission_classes = []
    def post(self, request, *args, **kwargs):
        """
        Refreshes the access token using the provided refresh token.
        """
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            raise AuthenticationFailed('Refresh token is required')

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
        except Exception as e:
            raise AuthenticationFailed('Invalid refresh token')

        return Response({
            'access': new_access_token,
        }, status=status.HTTP_200_OK)

class SignupView(APIView):
    """
    API view to sign up a user.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        """
        Signs up a user with the provided username and password.
        """
        user = request.user
        if not user.is_authenticated:
            raise AuthenticationFailed('User is not authenticated')

        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'message': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)

            if user is None:
                raise AuthenticationFailed('User already exists with that username or password is incorrect')
            
        user.username = username
        user.set_password(password)
        user.save()

        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        

        return Response({
            'message': 'User signed up successfully.',
            'refresh_token': str(refresh_token),
            'access_token': access_token
        }, status=status.HTTP_201_CREATED)

class ProfileView(APIView):
    """
    API view to retrieve the user profile.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        """
        Retrieves the user profile information, including username, high score, and games played.
        """
        user = request.user
        if not user.is_authenticated:
            raise AuthenticationFailed('User is not authenticated')

        user_high_score = Game.get_player_high_score(user)
        return Response({
            'username': user.username,
            'high_score': user_high_score.correct_answers if user_high_score else 0,
            'games_played': Game.objects.filter(player=user).count(),
        }, status=status.HTTP_200_OK)

class AdminTokenView(APIView):
    """
    API view to generate tokens for admin users.
    """
    permission_classes = []
    def post(self, request, *args, **kwargs):
        """
        Generates a refresh and access token for admin users.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None or not user.is_superuser:
            raise AuthenticationFailed('Invalid credentials or not a superuser')

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class AddDestinationView(APIView):
    """
    API view to add a new destination.
    """
    permission_classes = [IsAdminUser]
    def post(self, request, *args, **kwargs):
        """
        Adds a new destination with the provided city, country, clues, fun facts, and trivia.
        """
        data = request.data

        if not data:
            return Response({'message': 'Data is required.'}, status=status.HTTP_400_BAD_REQUEST)

        city = data.get('city')
        country = data.get('country')
        clues = data.get('clues')
        fun_facts = data.get('fun_facts')
        trivia = data.get('trivia')

        if not city:
            return Response({'message': 'City is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not country:
            return Response({'message': 'Country is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not clues:
            return Response({'message': 'Clues are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not fun_facts:
            return Response({'message': 'Fun facts are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not trivia:
            return Response({'message': 'Trivia are required.'}, status=status.HTTP_400_BAD_REQUEST)

        destination, created = Destination.objects.get_or_create(city=city, country=country)

        for clue in clues:
            DestinationInfo.objects.create(destination=destination, info=clue, type=DestinationInfo.InfoType.CLUE)

        for fact in fun_facts:
            DestinationInfo.objects.create(destination=destination, info=fact, type=DestinationInfo.InfoType.FUN_FACT)

        for trivium in trivia:
            DestinationInfo.objects.create(destination=destination, info=trivium, type=DestinationInfo.InfoType.TRIVIA)

        return Response({
            'message': 'Destination and related info created successfully.',
            'data': {
                'city': city,
                'country': country,
                'clues': clues,
                'fun_facts': fun_facts,
                'trivia': trivia
            }
        }, status=status.HTTP_201_CREATED)

class NewGameView(APIView):
    """
    API view to create a new game.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        """
        Creates a new game for the authenticated user.
        """
        user = request.user
        if not user.is_authenticated:
            raise AuthenticationFailed('User is not authenticated')
        game = Game.objects.create(player=user)
        return Response({
            'game_id': str(game.id),
        }, status=status.HTTP_201_CREATED)

class GameQuestionsView(APIView):
    """
    API view to retrieve questions for a game.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, game_id, *args, **kwargs):
        """
        Retrieves the clues for the current question in the specified game.
        """
        user = request.user
        if not user.is_authenticated:
            raise AuthenticationFailed('User is not authenticated')

        try:
            game = Game.objects.get(id=game_id, player=user)
        except Game.DoesNotExist:
            return Response({'detail': 'Game not found.'}, status=status.HTTP_404_NOT_FOUND)

        question = Question.objects.filter(game=game, is_active=True).first()
        if not question:
            question = Question.new_question(game=game)
            if question is None:
                return Response({
                    'clues': [],
                    'is_active': False,
                }, status=status.HTTP_200_OK)

        clues = question.clues.all()
        return Response({
            'clues': [clue.info for clue in clues],
            'is_active': game.is_active,
        }, status=status.HTTP_200_OK)
    
class GameResponseView(APIView):
    """
    API view to submit a response to a game question.
    """
    serializer_class = serializers.Serializer
    def post(self, request, game_id, *args, **kwargs):
        """
        Submits a city name as a response to the current question and returns whether the answer is correct, the correct city, fun facts, and trivia.
        """
        user = request.user
        if not user.is_authenticated:
            raise AuthenticationFailed('User is not authenticated')
        game = Game.objects.get(id=game_id, player=user)
        question = Question.objects.filter(game=game, is_active=True).first()
        if question is None:
            return Response({
                'message': 'No active questions in the game.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        provided_city = request.data.get('city')
        if not provided_city:
            return Response({
                'message': 'City name is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        is_answered_correctly = (provided_city.lower() == question.destination.city.lower())
        question.is_answered_correctly = is_answered_correctly
        question.is_active = False
        question.save()
        
        return Response({
            'is_answered_correctly': is_answered_correctly,
            'correct_city': question.destination.city,
            'fun_facts': [info.info for info in DestinationInfo.objects.filter(destination=question.destination, type=DestinationInfo.InfoType.FUN_FACT)],
            'trivia': [info.info for info in DestinationInfo.objects.filter(destination=question.destination, type=DestinationInfo.InfoType.TRIVIA)],
        }, status=status.HTTP_200_OK)
    
class GameScoreView(APIView):
    """
    API view to retrieve the score for a game.
    """
    serializer_class = GameScoreSerializer
    authentication_classes = []
    def get(self, request, game_id, *args, **kwargs):
        """
        Retrieves the score for the specified game.
        """
        user = request.user
        if not user.is_authenticated:
            raise AuthenticationFailed('User is not authenticated')
        game = Game.objects.filter(id=game_id, player=user)
        if not game.exists():
            return Response({
                'correct_answers': 0,
                'total_questions': 0,
                'percentage': 0,
            }, status=status.HTTP_200_OK)
        game = game.first()
        serializer = GameScoreSerializer(game.get_score())
        return Response(serializer.data, status=status.HTTP_200_OK)

class GameHighScoreView(APIView):
    """
    API view to retrieve the global high score.
    """
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        """
        Retrieves the global high score.
        """
        # Return global high score
        game = Game.get_global_high_score()
        if isinstance(game, Game):
            score = game.get_score()
            return Response({
                'username': game.player.username,
                'high_score': score.correct_answers,
            }, status=status.HTTP_200_OK)
        return Response({
            'username': None,
            'high_score': 0,
        }, status=status.HTTP_200_OK)

class GameHighScoreUserView(APIView):
    """
    API view to retrieve a user's high score.
    """
    def get(self, request, username, *args, **kwargs):
        """
        Retrieves the high score for the specified user.
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        user_high_score = Game.get_player_high_score(user)
        return Response({
            'username': user.username,
            'high_score': user_high_score.correct_answers if user_high_score else 0,
        }, status=status.HTTP_200_OK)

class ListCitiesView(APIView):
    """
    API view to list all cities.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        """
        Lists all cities.
        """
        cities = Destination.objects.values_list('city', flat=True)
        return Response({'cities': list(cities)}, status=status.HTTP_200_OK)

import google.generativeai as genai
import os

class GenerateDestinationView(APIView):
    """
    API view to generate a new destination using Google GenAI.
    """
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        """
        Generates a new destination with the provided city using Google GenAI.
        """
        city = request.data.get('city')
        if not city:
            return Response({'message': 'City is required.'}, status=status.HTTP_400_BAD_REQUEST)

        genai.configure(api_key=os.environ.get('GOOGLE_GENAI_API_KEY'))
        model = genai.GenerativeModel('gemini-2.0-flash')

        prompt = f"Generate information about the city: {city}. Include 5 clues to guess the city, the country of the city, 4 fun facts, and 4 trivia statements (not questions). Keep it fun and engaging. For example, you can add emojis."
        prompt += "Respond with a JSON object with the following keys: city, country, clues, fun_facts, trivia.\n"
        prompt += "Example JSON:\n"
        prompt += "{\n"
        prompt += "  \"city\": \"City Name\",\n"
        prompt += "  \"country\": \"Country Name\",\n"
        prompt += "  \"clues\": [\"Clue 1\", \"Clue 2\", \"Clue 3\", \"Clue 4\", \"Clue 5\"],\n"
        prompt += "  \"fun_facts\": [\"Fun Fact 1\", \"Fun Fact 2\", \"Fun Fact 3\", \"Fun Fact 4\"],\n"
        prompt += "  \"trivia\": [\"Trivia 1\", \"Trivia 2\", \"Trivia 3\", \"Trivia 4\"]\n"
        prompt += "}\n"

        try:
            response = model.generate_content(prompt)
            content = response.text
            print(content)

            import json
            try:
                data = json.loads("".join(content.split('\n')[1:-1]))
                city = data.get('city')
                country = data.get('country')
                clues = data.get('clues', [])
                fun_facts = data.get('fun_facts', [])
                trivia = data.get('trivia', [])

                destination, created = Destination.objects.get_or_create(city=city, country=country)

                for clue in clues:
                    DestinationInfo.objects.create(destination=destination, info=clue, type=DestinationInfo.InfoType.CLUE)

                for fact in fun_facts:
                    DestinationInfo.objects.create(destination=destination, info=fact, type=DestinationInfo.InfoType.FUN_FACT)

                for trivium in trivia:
                    DestinationInfo.objects.create(destination=destination, info=trivium, type=DestinationInfo.InfoType.TRIVIA)

                return Response({
                    'message': 'Destination and related info created successfully using Google GenAI.',
                    'data': {
                        'city': city,
                        'country': country,
                        'clues': clues,
                        'fun_facts': fun_facts,
                        'trivia': trivia,
                    }
                }, status=status.HTTP_201_CREATED)
            except json.JSONDecodeError as e:
                return Response({'message': f'Error decoding JSON: {e}'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': f'Error generating destination: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
