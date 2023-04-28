# Generated by Django 4.2 on 2023-04-26 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import feed.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=10, unique=True)),
                ('caption', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=5)),
                ('views', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('likes', models.ManyToManyField(blank=True, related_name='media_likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='MediaFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.FileField(blank=True, null=True, upload_to=feed.models.get_media_filename, verbose_name='media_files')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('media', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='feed.media')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('likes', models.ManyToManyField(blank=True, related_name='reply_likes', to=settings.AUTH_USER_MODEL)),
                ('media', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='feed.media')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='CommentFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to=feed.models.get_comment_filename, verbose_name='media_files')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comment_files', to='feed.comments')),
            ],
        ),
    ]
