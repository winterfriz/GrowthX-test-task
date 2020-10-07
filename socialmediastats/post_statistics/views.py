from django.db.models import Sum
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .models import PostStatistics
from .serializers import PostStatisticsSerializer


class PostStatisticsCreate(CreateAPIView):
    serializer_class = PostStatisticsSerializer


@api_view(['GET'])
def latest_statistics_by_post(request, post_id):
    post_stats = (
        PostStatistics
        .objects
        .filter(post_id=post_id)
        .order_by('-created_at')
        .first()
    )
    if post_stats:
        serializer = PostStatisticsSerializer(post_stats)
        return Response(serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def latest_statistics_by_user(request, user_id):
    by_user = PostStatistics.objects.filter(user_id=user_id)
    latest_created_at = (
        by_user
        .order_by('-created_at')
        .values_list('created_at')
        .first()
    )
    if latest_created_at:
        likes_count_sum = (
            by_user
            .filter(created_at__date=latest_created_at[0].date())
            .aggregate(Sum('likes_count'))
        )
        data = {
            'user_id': user_id,
            'likes_count': likes_count_sum['likes_count__sum']
        }
        return Response(data)
    return Response(status=status.HTTP_404_NOT_FOUND)

