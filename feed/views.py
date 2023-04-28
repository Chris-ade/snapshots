from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, Http404
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.conf import settings
from .models import *
from .utils import *

image_types = ['image/jpeg', 'image/png', 'image/gif']
video_types = ['video/mp4', 'video/webm', 'video/mkv']

VID_MAX_UPLOAD_SIZE = 30 * 1024 * 1024 # 30MB
PIC_MAX_UPLOAD_SIZE = 5 * 1024 * 1024 # 5MB

@login_required
def feed(request):
    '''
    Displays the feeds page.

    Args:
        request (object): the HTTP request object

    Returns:
        A rendered template displaying all the posts available.

    Example:
        GET /feed/
    '''
    # Fetches all the media objects
    media_object = Media.objects.all()
    context = {
      'page_title': 'SnapShots - Share Your World Through Photos',
      'user': request.user,
      'posts': media_object,
    }
    # Renders the feed page
    return render(request, 'feed/feeds.html', context)

def view(request, link):
    '''
    Displays the overview of a post.

    Args:
        request (object): the HTTP request object
        link (str): the link of the post

    Returns:
        A rendered template displaying full details about the post.

    Example:
        GET /view/(:link)
    '''
    try:
        # Updates the number of views per request
        media_object = Media.objects.get(link=link)
        media_object.views += 1
        media_object.save()
        suggestions = Media.objects.exclude(pk=media_object.id)
        context = {
          'page_title': f'{media_object.caption} - Image on SnapShots',
          'base_url': settings.BASE_URL,
          'user': request.user,
          'post': media_object,
          'suggestions': suggestions,
        }
        # Renders the feed page
        return render(request, 'feed/view.html', context)
    except Media.DoesNotExist:
        return render(request, 'errors/404.html')

@login_required
def upload(request):
    '''
    Displays the upload page and process the uploaded files if request method is POST.

    Args:
        request (object): the HTTP request object

    Returns:
        A rendered template of the file upload page.

    Example:
        GET, POST /upload/
    '''
    # Checks if request method is POST
    if request.method == 'POST':
        file = request.FILES.get('file')
        caption = request.POST.get('caption')
        # Checks if there is a file present with a caption
        if not file or not caption:
            # Returns an error as JSON
            return JsonResponse({'status': 201, 'message': 'An error occurred!'})
        try:
            # Checks if file matches an image type
            if file.content_type in image_types:
                if file.size > PIC_MAX_UPLOAD_SIZE:
                    raise ValidationError('Maximum limit exceeded!')
                type = "image"
            # Checks if file matches a video type
            elif file.content_type in video_types:
                if file.size > VID_MAX_UPLOAD_SIZE:
                    raise ValidationError('Maximum limit exceeded!')
                type = "video"
            # Generate a unique link for the media object
            link = generate_random_string(7)
            # Creates a new media object with type of image
            media = Media.objects.create(user=request.user, caption=caption, link=link)
            # Saves the object
            media.save()
            file_obj = MediaFiles.objects.create(media=media, type=type, url=file)
            # Returns success message as JSON
            return JsonResponse({'status': 200,  'message': 'File uploaded successfully'})
        except ValidationError:
            return JsonResponse({'status': 201,  'message': 'File size exceeds the limit!'})
    else:
        context = {
          'page_title': 'Upload - SnapShots',
        }
        # Renders the feed page
        return render(request, 'feed/upload.html', context)

@login_required
def like(request):
    '''
    Function for liking a post

    Args:
        request (object): the HTTP request object

    Returns:
        A JSON object with the a message indicating if the action was successful or not.
        If request method is not POST, displays an error page

    Example:
        POST /like/
    '''
    # Checks if request method is POST
    if request.method == 'POST':
        media_id = request.POST.get('target')
        # Checks if media_id is int
        if not media_id:
            # Returns an error as JSON
            return JsonResponse({'status': 201, 'message': 'An error occurred!'})
        try:
            # Fetch the media object
            obj = Media.objects.get(pk=media_id)
            is_liked = obj.likes.filter(id=request.user.id).exists()
            message = ''
            status = ''
            if not is_liked:
                # Adds the user to the likes table
                obj.likes.add(request.user)
                message = 'Liked!'
                status = 1
                count = obj.likes.count()
            else:
                # Deletes the user like
                obj.likes.remove(request.user)
                message = 'Unliked!'
                status = 0
                count = obj.likes.count()
            # Returns a success message
            return JsonResponse({'status': 200, 'action': status, 'count': count, 'message': message})
        except Media.DoesNotExist:
            # Returns an error message
            return JsonResponse({'status': 201,  'message': 'An error occurred!'})
    # If request method is not POST, display an error page
    return render(request, 'errors/404.html')

@login_required
def comment(request):
    '''
    Function for adding comments to a post

    Args:
        request (object): the HTTP request object

    Returns:
        A JSON object with the newly created comment and a message indicating if the action was successful or not.
        If request method is not POST, displays an error page.

    Example:
        POST /comment/
    '''
    # Checks if request method is POST
    if request.method == 'POST':
        media_id = request.POST.get('target')
        content = request.POST.get('comment')
        media = request.FILES.get('media')
        # Checks if media_id is set
        if not media_id and not comment:
            # Returns an error as JSON
            return JsonResponse({'status': 201, 'message': 'An error occurred!'})
        try:
            # Fetch the media object
            media_obj = Media.objects.get(link=media_id)
            # Creates a new comment object
            comment_obj = Comments.objects.create(media=media_obj, user=request.user, content=content)
            # Checks if a file was sent
            if media:
                # Checks if the file sent is really an image
                if media.content_type in image_types:
                    # Checks if the file size is larger than the upload limit
                    if media.size > PIC_MAX_UPLOAD_SIZE:
                        # Returns an error
                        return JsonResponse({'status': 201,  'message': 'The selected image is larger than the upload limit!'})
                # Creates a new comment image object
                comment_image_obj = CommentFile.objects.create(comment=comment_obj, image=media)
            # Renders the comment template to string to be sent back to the front end
            comment = render_to_string('feed/comment.html', {'comment': comment_obj, 'post': media_obj})
            # Returns the output
            return JsonResponse({'status': 200, 'message': 'Posted!', 'comment': comment, 'count': media_obj.replies.count()})
        except Media.DoesNotExist:
            # Returns an error message
            return JsonResponse({'status': 201,  'message': 'An error occurred!'})
    # If request method is not POST, display an error page
    return render(request, 'errors/404.html')

@login_required
def likeComment(request):
    '''
    Function for liking a comment

    Args:
        request (object): the HTTP request object

    Returns:
        A JSON object with the a message indicating if the action was successful or not.
        If request method is not POST, displays an error page

    Example:
        POST /like/
    '''
    # Checks if request method is POST
    if request.method == 'POST':
        comment_id = request.POST.get('target')
        # Checks if comment_id value is set
        if not comment_id:
            # Returns an error as JSON
            return JsonResponse({'status': 201, 'message': 'An error occurred!'})
        try:
            # Fetch the media object
            obj = Comments.objects.get(pk=comment_id)
            is_liked = obj.likes.filter(id=request.user.id).exists()
            message = ''
            status = ''
            if not is_liked:
                # Adds the user to the likes table
                obj.likes.add(request.user)
                message = 'Liked!'
                status = 1
                count = obj.likes.count()
            else:
                # Deletes the user like
                obj.likes.remove(request.user)
                message = 'Unliked!'
                status = 0
                count = obj.likes.count()
            # Returns a success message
            return JsonResponse({'status': 200, 'action': status, 'count': count, 'message': message})
        except Comments.DoesNotExist:
            # Returns an error message
            return JsonResponse({'status': 201,  'message': 'An error occurred!'})
    # If request method is not POST, display an error page
    return render(request, 'errors/404.html')
