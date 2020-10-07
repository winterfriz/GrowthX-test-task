from rest_framework import serializers

from .models import PostStatistics


class PostStatisticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostStatistics
        fields = ['post_id', 'user_id', 'likes_count']


