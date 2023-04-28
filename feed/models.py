from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

# Load the users model
User = get_user_model()

def get_media_filename(instance, filename):
    '''
    Gets the filename for the media object
    '''
    media_id = instance.media.id
    if instance.type == "image":
        return f"feeds/images/{media_id}/{filename}"
    else:
        return f"feeds/videos/{media_id}/{filename}"

def get_comment_filename(instance, filename):
    '''
    Gets the filename for the media object
    '''
    comment_id = instance.comment.id
    return f"comments/{comment_id}/{filename}"

class Media(models.Model):
    '''
    Model responsible for storing data
    '''
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    link = models.CharField(max_length=10, unique=True)
    caption = models.CharField(max_length=50)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, blank=True, related_name="media_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        '''
        Returns a string representation of the media object
        '''
        return self.caption

class MediaFiles(models.Model):
    '''
    Model responsible for storing media files data
    '''
    media = models.ForeignKey(Media, default=None, related_name="files", on_delete=models.CASCADE)
    type = models.CharField(max_length=5)
    url = models.FileField(upload_to=get_media_filename, verbose_name='media_files', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    '''
    Model responsible for storing media replies
    '''
    media = models.ForeignKey(Media, default=None, related_name="replies", on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    likes = models.ManyToManyField(User, blank=True, related_name="reply_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        '''
        Returns a string representation of the media object
        '''
        return self.content

class CommentFiles(models.Model):
    '''
    Model responsible for storing comment files data
    '''
    comment = models.ForeignKey(Comments, default=None, related_name="comment_files", on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_comment_filename, verbose_name='comment_files', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
