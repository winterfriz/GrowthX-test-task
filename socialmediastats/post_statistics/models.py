from django.db import models


class PostStatistics(models.Model):
    post_id = models.CharField(
        max_length=10,
        null=False,
        blank=False,
    )
    user_id = models.CharField(
        max_length=10,
        null=False,
        blank=False,
    )
    likes_count = models.PositiveBigIntegerField(
        null=False,
    )


