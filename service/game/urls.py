from django.urls import path
from .views import UnregisteredUserTokenView, UnregisteredUserTokenRefreshView, NewGameView, GameQuestionsView, AddDestinationView, AdminTokenView, GameResponseView, GameHighScoreView, GameHighScoreUserView
from .views import GameScoreView, SignupView, ProfileView, ListCitiesView, GenerateDestinationView, LeaderboardView

urlpatterns = [
    path('token/', UnregisteredUserTokenView.as_view(), name='unregistered_user_token'),
    path('token/refresh/', UnregisteredUserTokenRefreshView.as_view(), name='unregistered_user_token_refresh'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('game/', NewGameView.as_view(), name='new_game'),
    path('game/<str:game_id>/questions/', GameQuestionsView.as_view(), name='game_questions'),
    path('game/<str:game_id>/response/', GameResponseView.as_view(), name='game_response'),
    path('game/<str:game_id>/score/', GameScoreView.as_view(), name='game_score'),
    path('destination/', AddDestinationView.as_view(), name='add_destination'),
    path('admin/token/', AdminTokenView.as_view(), name='admin_token'),
    path('cities/', ListCitiesView.as_view(), name='list_cities'),
    path('game/high_score/', GameHighScoreView.as_view(), name='game_high_score'),
    path('game/high_score/<str:username>/', GameHighScoreUserView.as_view(), name='game_high_score_user'),
    path('destination/generate/', GenerateDestinationView.as_view(), name='generate_destination'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]
