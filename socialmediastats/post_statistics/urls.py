from django.urls import path

from .views import PostStatisticsCreate, latest_statistics_by_post, latest_statistics_by_user

app_name = 'post_statistics'
urlpatterns = [
    path('', PostStatisticsCreate.as_view(), name='post-statistics-create'),
    path('posts/<str:post_id>/latest', latest_statistics_by_post, name='latest-statistics-by-post'),
    path('users/<str:user_id>/latest', latest_statistics_by_user, name='latest-statistics-by-user'),
]
