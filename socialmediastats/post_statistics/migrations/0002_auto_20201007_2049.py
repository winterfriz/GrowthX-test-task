# Generated by Django 3.1 on 2020-10-07 20:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('post_statistics', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poststatistics',
            options={'get_latest_by': 'created_at'},
        ),
        migrations.AddField(
            model_name='poststatistics',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
