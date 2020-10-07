from datetime import datetime, timedelta

from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework.views import status

from .models import PostStatistics


def get_now_datetime():
    return datetime.now(tz=timezone.utc)


class PostStatisticsCreateAPIViewTest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('post_statistics:post-statistics-create')

    def test_create_post_statistics(self):
        self.assertEquals(
            PostStatistics.objects.count(),
            0
        )
        data = {
            'post_id': '1',
            'user_id': '1',
            'likes_count': 10
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(
            PostStatistics.objects.count(),
            1
        )
        post = PostStatistics.objects.first()
        self.assertEquals(
            post.post_id,
            data['post_id']
        )
        self.assertEquals(
            post.user_id,
            data['user_id']
        )
        self.assertEquals(
            post.likes_count,
            data['likes_count']
        )


class LatestStatisticsByPostAPIViewTest(APITestCase):

    @staticmethod
    def _get_url(post_id):
        return reverse('post_statistics:latest-statistics-by-post', args=(post_id,))

    def test_get_statistics_by_post_not_found(self):
        post_id = '1'
        url = self._get_url(post_id)
        response = self.client.get(url)
        self.assertEquals(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_get_statistics_by_post_today_latest(self):
        post_id = '1'
        now_stats = PostStatistics(
            post_id=post_id,
            user_id='1',
            likes_count=5,
        )
        now_stats.save()
        yesterday_stats = PostStatistics(
            post_id=post_id,
            user_id='2',
            likes_count=10,
        )
        yesterday_stats.save()
        yesterday_stats.created_at = get_now_datetime() - timedelta(days=1)
        yesterday_stats.save(update_fields=['created_at'])
        print(now_stats.created_at)
        print(yesterday_stats.created_at)
        url = self._get_url(post_id)
        response = self.client.get(url)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.json()
        self.assertEquals(
            data['post_id'],
            post_id,
        )
        self.assertEquals(
            data['user_id'],
            now_stats.user_id
        )
        self.assertEquals(
            data['likes_count'],
            now_stats.likes_count
        )

    def test_get_statistics_by_post_yesterday_latest(self):
        post_id = '1'
        yesterday_stats = PostStatistics(
            post_id=post_id,
            user_id='2',
            likes_count=10,
        )
        yesterday_stats.save()
        yesterday_stats.created_at = get_now_datetime() - timedelta(days=1)
        yesterday_stats.save(update_fields=['created_at'])

        url = self._get_url(post_id)
        response = self.client.get(url)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.json()
        self.assertEquals(
            data['post_id'],
            post_id,
        )
        self.assertEquals(
            data['user_id'],
            yesterday_stats.user_id
        )
        self.assertEquals(
            data['likes_count'],
            yesterday_stats.likes_count
        )


class LatestStatisticsByUserAPIViewTest(APITestCase):

    @staticmethod
    def _get_url(user_id):
        return reverse('post_statistics:latest-statistics-by-user', args=(user_id,))

    def test_get_statistics_by_user_not_found(self):
        user_id = '1'
        url = self._get_url(user_id)
        response = self.client.get(url)
        self.assertEquals(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_get_statistics_by_user_today_latest(self):
        user_id = '1'
        now_stats_1 = PostStatistics(
            post_id='1',
            user_id=user_id,
            likes_count=5,
        )
        now_stats_1.save()
        now_stats_2 = PostStatistics(
            post_id='2',
            user_id=user_id,
            likes_count=10,
        )
        now_stats_2.save()

        yesterday_stats = PostStatistics(
            post_id='3',
            user_id=user_id,
            likes_count=10,
        )
        yesterday_stats.save()
        yesterday_stats.created_at = get_now_datetime() - timedelta(days=1)
        yesterday_stats.save(update_fields=['created_at'])

        url = self._get_url(user_id)
        response = self.client.get(url)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )
        data = response.json()
        self.assertEquals(
            data['user_id'],
            user_id,
        )
        self.assertEquals(
            data['likes_count'],
            now_stats_1.likes_count + now_stats_2.likes_count,
        )

    def test_get_statistics_by_user_yesterday_latest(self):
        user_id = '1'
        yesterday_stats_1 = PostStatistics(
            post_id='1',
            user_id=user_id,
            likes_count=5,
        )
        yesterday_stats_1.save()
        yesterday_stats_1.created_at = get_now_datetime() - timedelta(days=1)
        yesterday_stats_1.save(update_fields=['created_at'])
        yesterday_stats_2 = PostStatistics(
            post_id='1',
            user_id=user_id,
            likes_count=5,
        )
        yesterday_stats_2.save()
        yesterday_stats_2.created_at = get_now_datetime() - timedelta(days=1)
        yesterday_stats_2.save(update_fields=['created_at'])

        url = self._get_url(user_id)
        response = self.client.get(url)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )
        data = response.json()
        self.assertEquals(
            data['user_id'],
            user_id,
        )
        self.assertEquals(
            data['likes_count'],
            yesterday_stats_1.likes_count + yesterday_stats_2.likes_count,
        )