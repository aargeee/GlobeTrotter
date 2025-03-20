import random
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Game, Question, Destination, DestinationInfo
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

class GameFlowTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.destination1 = Destination.objects.create(city='City1', country='Country1')
        self.destination2 = Destination.objects.create(city='City2', country='Country2')
        self.clue1 = DestinationInfo.objects.create(destination=self.destination1, info='Clue 1', type=DestinationInfo.InfoType.CLUE)
        self.clue2 = DestinationInfo.objects.create(destination=self.destination1, info='Clue 2', type=DestinationInfo.InfoType.CLUE)
        self.clue3 = DestinationInfo.objects.create(destination=self.destination2, info='Clue 3', type=DestinationInfo.InfoType.CLUE)
        self.clue4 = DestinationInfo.objects.create(destination=self.destination2, info='Clue 4', type=DestinationInfo.InfoType.CLUE)

    def test_create_new_game(self):
        game = Game.objects.create(player=self.user)
        self.assertEqual(game.player, self.user)

    def test_present_existing_question(self):
        game = Game.objects.create(player=self.user)
        question = Question.new_question(game=game)
        question.is_answered_correctly = False
        question.save()

        unanswered_question = Question.objects.filter(game=game, is_answered_correctly=False).first()
        self.assertIsNotNone(unanswered_question)
        self.assertEqual(unanswered_question, question)

    def test_create_new_question_if_none_unanswered(self):
        game = Game.objects.create(player=self.user)
        question = Question.new_question(game=game)
        question.is_answered_correctly = True
        question.save()

        unanswered_question = Question.objects.filter(game=game, is_answered_correctly=False).first()
        self.assertIsNone(unanswered_question)

        new_question = Question.new_question(game=game)

        self.assertIsNotNone(new_question)
        self.assertEqual(new_question.game, game)
        self.assertFalse(new_question.is_answered_correctly)
        self.assertEqual(new_question.clues.count(), 2)

    def test_game_score(self):
        game = Game.objects.create(player=self.user)
        question1 = Question.new_question(game=game)
        question1.is_answered_correctly = True
        question1.save()
        question2 = Question.new_question(game=game)
        question2.is_answered_correctly = False
        question2.save()

        score = game.get_score()
        self.assertEqual(score.correct_answers, 1)
        self.assertEqual(score.total_questions, 2)
        self.assertEqual(score.percentage, 50)

    def test_get_player_high_score(self):
        game1 = Game.objects.create(player=self.user)
        question1 = Question.new_question(game=game1)
        question1.is_answered_correctly = True
        question1.save()
        question2 = Question.new_question(game=game1)
        question2.is_answered_correctly = False
        question2.save()

        game2 = Game.objects.create(player=self.user)
        question3 = Question.new_question(game=game2)
        question3.is_answered_correctly = True
        question3.save()
        question4 = Question.new_question(game=game2)
        question4.is_answered_correctly = True
        question4.save()

        high_score = Game.get_player_high_score(self.user)
        self.assertEqual(high_score.correct_answers, 2)
        self.assertEqual(high_score.total_questions, 2)
        self.assertEqual(high_score.percentage, 100)

class GameViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.admin_user = User.objects.create_superuser(username='admin', password='12345')
        self.destination1 = Destination.objects.create(city='City1', country='Country1')
        self.destination2 = Destination.objects.create(city='City2', country='Country2')
        self.clue1 = DestinationInfo.objects.create(destination=self.destination1, info='Clue 1', type=DestinationInfo.InfoType.CLUE)
        self.clue2 = DestinationInfo.objects.create(destination=self.destination1, info='Clue 2', type=DestinationInfo.InfoType.CLUE)
        self.clue3 = DestinationInfo.objects.create(destination=self.destination2, info='Clue 3', type=DestinationInfo.InfoType.CLUE)
        self.clue4 = DestinationInfo.objects.create(destination=self.destination2, info='Clue 4', type=DestinationInfo.InfoType.CLUE)

    def get_access_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_unregistered_user_token(self):
        url = reverse('unregistered_user_token')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_unregistered_user_token_refresh(self):
        url = reverse('unregistered_user_token')
        response = self.client.post(url)
        refresh_token = response.data['refresh']

        url = reverse('unregistered_user_token_refresh')
        response = self.client.post(url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_signup(self):
        access_token = self.get_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('signup')
        response = self.client.post(url, {'username': 'newuser', 'password': 'newpassword'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_signup_existing_user_incorrect_password(self):
        access_token = self.get_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('signup')
        User.objects.create_user(username='existinguser', password='correctpassword')
        response = self.client.post(url, {'username': 'existinguser', 'password': 'incorrectpassword'})
        self.assertEqual(response.status_code, 401)

    def test_profile(self):
        access_token = self.get_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.user.username)

    def test_admin_token(self):
        url = reverse('admin_token')
        response = self.client.post(url, {'username': 'admin', 'password': '12345'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_admin_token_not_superuser(self):
        url = reverse('admin_token')
        User.objects.create_user(username='notadmin', password='12345')
        response = self.client.post(url, {'username': 'notadmin', 'password': '12345'})
        self.assertEqual(response.status_code, 401)

    def test_add_destination(self):
        access_token = self.get_access_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('add_destination')
        response = self.client.post(url, {'city': 'NewCity', 'country': 'NewCountry', 'clues': ['Clue1', 'Clue2'], 'fun_facts': ['Fact1'], 'trivia': ['Trivia1']})
        self.assertEqual(response.status_code, 201)

    def test_new_game(self):
        access_token = self.get_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('new_game')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)
        self.assertIn('game_id', response.data)

    def test_game_questions(self):
        access_token = self.get_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        game = Game.objects.create(player=self.user)
        url = reverse('game_questions', kwargs={'game_id': str(game.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('clues', response.data)
        self.assertIn('is_active', response.data)

    def test_game_response(self):
        access_token = self.get_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        game = Game.objects.create(player=self.user)
        question = Question.new_question(game=game)
        url = reverse('game_response', kwargs={'game_id': str(game.id)})
        response = self.client.post(url, {'city': question.destination.city})
        self.assertEqual(response.status_code, 200)
        self.assertIn('is_answered_correctly', response.data)
        self.assertIn('correct_city', response.data)
        self.assertIn('fun_facts', response.data)
        self.assertIn('trivia', response.data)

    def test_game_score_view(self):
        access_token = self.get_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        game = Game.objects.create(player=self.user)
        question = Question.new_question(game=game)
        question.is_answered_correctly = True
        question.save()
        url = reverse('game_score', kwargs={'game_id': str(game.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('correct_answers', response.data)
        self.assertIn('total_questions', response.data)
        self.assertIn('percentage', response.data)

    def test_game_high_score_view(self):
        access_token = self.get_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        game = Game.objects.create(player=self.user)
        question = Question.new_question(game=game)
        question.is_answered_correctly = True
        question.save()
        url = reverse('game_high_score')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.data)
        self.assertIn('high_score', response.data)

    def test_game_high_score_view_user_not_found(self):
        access_token = self.get_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('game_high_score_user', kwargs={'username': 'nonexistentuser'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_list_cities_view(self):
        access_token = self.get_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('list_cities')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('cities', response.data)

class GameFlowTestsModels(TestCase):
    def test_get_global_high_score_no_questions(self):
        high_score = Game.get_global_high_score()
        self.assertEqual(high_score.correct_answers, 0)
        self.assertEqual(high_score.total_questions, 0)
        self.assertEqual(high_score.percentage, 0)
