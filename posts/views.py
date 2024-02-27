import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import LostPostForm, FoundPostForm, FileFieldForm
from .models import LostPost, FoundPost, LostPhoto, FoundPhoto
from .models import Post


@login_required
def create_post(request):
    """
    Handle the creation of a new post, either 'lost' or 'found', including
    saving of related photos.

    Args:
    - request: HttpRequest object containing post data and files.

    Returns:
    - HttpResponse object redirecting to the homepage upon successful creation
      or renders the 'create_post.html' template with forms for creation.
    """
    # Retrieve the Google Maps API key from environment variables
    google_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    # Determine the post type ('lost' or 'found') from POST data
    post_type = request.POST.get('post_type')
    # Choose the appropriate form class based on the post type
    form_class = LostPostForm if post_type == 'lost' else FoundPostForm

    if request.method == 'POST':
        # Instantiate the forms with POST data and files
        form = form_class(request.POST)
        image_form = FileFieldForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            # Save the post instance without committing to the database
            post_instance = form.save(commit=False)
            post_instance.user = request.user  # Set the post's user
            post_instance.save()  # Save the post instance to the database

            # Determine the photo model class and kwargs based on post type
            if post_type == 'lost':
                photo_model_class = LostPhoto
                photo_kwargs = {'lost_post': post_instance}
            else:  # post_type == 'found'
                photo_model_class = FoundPhoto
                photo_kwargs = {'found_post': post_instance}

            # Save each uploaded photo instance
            for file in request.FILES.getlist('file_field'):
                photo_instance = photo_model_class(image=file, caption='',
                                                   **photo_kwargs)
                photo_instance.save()

            return redirect('/')
        else:
            print(form.errors)  # Print form errors to the console
    else:
        # Instantiate the forms without data if request method is not POST
        form = form_class()
        image_form = FileFieldForm()

    return render(request, 'create_post.html', {
        'form': form,
        'image_form': image_form,
        'post_type': post_type,
        'GOOGLE_MAPS_API_KEY': google_api_key
    })


def generic_search(model, search_query):
    """
    Perform a generic search on a given model based on the search query.

    Parameters:
    - model: The Django model class to search in.
    - search_query: The search term as a string.

    Returns:
    - A queryset of the search results.
    """
    if search_query:
        query = Q(title__icontains=search_query) | Q(
            description__icontains=search_query)
        results = model.objects.filter(query)
    else:
        results = model.objects.all()

    return results


ITEMS_PER_PAGE_OPTIONS = [5, 10, 20, 50]


def paginate_queryset(request, queryset, items_per_page=10):
    """
    Paginate a queryset and return the page object for the current request.
    """
    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def view_all_posts_list(request):
    """
    Display all posts (both LostPost and FoundPost) with optional search
    functionality and pagination, utilizing Django Polymorphic for combined
    querying.
    """
    search_query = request.GET.get('search_query', '')
    google_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')

    # Utilize polymorphism to fetch combined posts
    all_posts = Post.objects.all().instance_of(Post).order_by(
        '-created_at')  # Here we order the posts

    if search_query:
        all_posts = all_posts.filter(
            Q(title__icontains=search_query) | Q(
                description__icontains=search_query)
        )
    # Paginate the combined queryset
    paginated_posts = paginate_queryset(request, all_posts, items_per_page=10)
    search_url = reverse('posts:view_all_posts')

    context = {
        'GOOGLE_API_KEY': google_api_key,
        'posts': paginated_posts,
        'is_authenticated': request.user.is_authenticated,
        'active_tab': 'all',
        'items_per_page_options': ITEMS_PER_PAGE_OPTIONS,
        'search_query': search_query,
        'search_url': search_url,
    }

    return render(request, 'view_all_posts_list.html', context)


def view_lost_posts(request):
    """
    Display all lost posts with optional search functionality and pagination.
    """

    search_query = request.GET.get('search_query', '')
    lost_posts = generic_search(LostPost, search_query)
    # Correct the argument name to items_per_page
    paginated_posts = paginate_queryset(request, lost_posts, items_per_page=10)
    search_url = reverse('posts:view_lost_posts')

    context = {
        'posts': paginated_posts,
        'is_authenticated': request.user.is_authenticated,
        'active_tab': 'lost',
        'items_per_page_options': ITEMS_PER_PAGE_OPTIONS,
        'search_query': search_query,
        'search_url': search_url,
    }
    return render(request, 'view_all_posts_list.html', context)


def view_found_posts(request):
    """
    Display all found posts with optional search functionality and pagination.
    """
    search_query = request.GET.get('search_query', '')
    found_posts = generic_search(FoundPost, search_query)
    # Correct the argument name to items_per_page
    paginated_posts = paginate_queryset(request, found_posts, items_per_page=10)
    search_url = reverse('posts:view_found_posts')

    context = {
        'posts': paginated_posts,
        'is_authenticated': request.user.is_authenticated,
        'active_tab': 'found',
        'items_per_page_options': ITEMS_PER_PAGE_OPTIONS,
        'search_query': search_query,
        'search_url': search_url
    }
    return render(request, 'view_all_posts_list.html', context)


def post_detail_view(request, slug, post_type):
    """
    Renders the details page for a specific post, identified by its slug and
    type. It also determines whether the current user is the owner of the
    post to conditionally display edit and delete options.

    Args:
    - request: HttpRequest object containing metadata about the request.
    - slug: A string representing the unique slug of the post.
    - post_type: A string indicating the type of the post ('lost' or 'found').

    The function fetches the specified post using the slug and type to
    differentiate between lost and found posts. It then queries for
    associated photos and checks if the currently logged-in user is the owner
    of the post. This information, along with the Google Maps API key for
    rendering location maps, is passed to the template.

    Returns: - HttpResponse object rendering the 'post_details.html' template
    with the post details, associated photos, owner status, and Google Maps
    API key.
    """
    # Fetch the Google Maps API key from environment variables
    google_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    post = None

    # Determine the correct model based on the post type
    model = LostPost if post_type == 'lost' else FoundPost
    # Retrieve the specific post by slug, ensuring it exists

    try:
        if model == LostPost:
            post = get_object_or_404(LostPost, slug=slug)
        else:
            post = get_object_or_404(FoundPost, slug=slug)
    except ObjectDoesNotExist:  # we know it is post as it redirected her,
        # so by knowing
        # slug lets try to get out post ID and then pull it from database
        match_chars = ""
        reversed_slug = slug[::-1]
        reversed_slug_skip_second = reversed_slug[2:]
        for char in reversed_slug_skip_second:
            if char == '-':
                break
            match_chars = match_chars + str(char)
        match = match_chars[::-1]
        try:
            if post_type == 'lost':
                post = get_object_or_404(LostPost, pk=match)
            elif post_type == 'found':
                post = get_object_or_404(FoundPost, pk=match)
        except ObjectDoesNotExist:
            return render(request, '404.html')

    # Check if the current user is the owner of the post
    is_owner = request.user == post.user

    # Determine the correct photo model and fetch associated photos
    photo_model = LostPhoto if post_type == 'lost' else FoundPhoto
    photos = photo_model.objects.filter(
        lost_post=post) if post_type == 'lost' else photo_model.objects.filter(
        found_post=post)

    # Render the post details template with the relevant context
    return render(request, 'post_details.html', {
        'post_type': post_type,
        # Indicates whether it's a 'lost' or 'found' post
        'post': post,  # The post object containing its details
        'photos': photos,  # List of associated photo objects
        'is_owner': is_owner,
        # Boolean indicating if the current user is the post owner
        'GOOGLE_MAPS_API_KEY': google_api_key
        # API key for Google Maps integration
    })


@login_required
def update_post(request, slug, post_type):
    """
    Allows authenticated users to update their posts. It supports updating
    the post's details and associated images. Only the owner of the post can
    make updates.

    Args:
    - request: HttpRequest object containing metadata about the request.
    - slug: A string representing the unique slug of the post.
    - post_type: A string indicating the type of the post ('lost' or 'found').

    The function first checks if the current user is the owner of the post.
    If not, it redirects to a different page or shows an error message. It
    then processes the form submission for both the post details and the
    associated images. If the form submission is valid, it updates the post
    and associated images.

    Returns: - HttpResponse object rendering the 'update_post.html' template
    for GET requests or the 'post_details.html' template for successful POST
    requests, with the necessary context. - Redirects to a different page or
    shows an error if the user is not the post owner.
    """
    # Define model and form classes based on the post type
    model_class = LostPost if post_type == 'lost' else FoundPost
    photo_model_class = LostPhoto if post_type == 'lost' else FoundPhoto
    form_class = LostPostForm if post_type == 'lost' else FoundPostForm

    # Fetch the Google Maps API key from environment variables
    google_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')

    # Ensure the post exists and belongs to the current user
    post_instance = get_object_or_404(model_class, slug=slug, user=request.user)

    # Fetch associated photos for display
    photos = photo_model_class.objects.filter(
        **{'lost_post': post_instance} if post_type == 'lost' else {
            'found_post': post_instance})

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=post_instance)
        image_form = FileFieldForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            updated_post = form.save()

            # Save uploaded images
            for file in request.FILES.getlist('file_field'):
                photo_model_class.objects.create(image=file, **{
                    'lost_post': updated_post} if post_type == 'lost' else {
                    'found_post': updated_post})

            # Redirect to the updated post's detail view
            detail_url_name = 'posts:lost_post_details' if post_type == 'lost' else 'posts:found_post_details'

            return redirect(detail_url_name, slug=updated_post.slug,
                            post_type=post_type)
        else:
            # Handle form errors
            print(form.errors)
    else:
        # Initialize forms for GET request
        form = form_class(instance=post_instance)
        image_form = FileFieldForm()

    return render(request, 'update_post.html', {
        'form': form,
        'image_form': image_form,
        'photos': photos,
        'post_type': post_type,
        'GOOGLE_MAPS_API_KEY': google_api_key
    })


def delete_photo(request, photo_id, post_type):
    """
    Deletes a photo based on its ID and associated post type ('lost' or
    'found').

    Args:
    - request: HttpRequest object.
    - photo_id: The ID of the photo to delete.
    - post_type: A string indicating the type of post ('lost' or 'found').

    Returns:
    - HttpResponse redirecting to the post detail page after deletion.
    """
    # Determine if it's a LostPhoto or FoundPhoto based on the post_type
    if post_type == 'lost':
        photo = get_object_or_404(LostPhoto, pk=photo_id)
    elif post_type == 'found':
        photo = get_object_or_404(FoundPhoto, pk=photo_id)
    else:
        # Redirect to a default or error page if post_type is invalid
        return redirect('/error-page/')  # Adjust this URL as needed

    # Perform the deletion, which includes Cloudinary asset deletion via
    # overridden delete method
    photo.delete()

    try:
        # Assuming the deletion code is here
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def map_all_posts(request):
    """
    Display all posts (both LostPost and FoundPost) with optional search
    functionality and pagination, utilizing Django Polymorphic for combined
    querying.
    """
    search_query = request.GET.get('search_query', '')

    # Utilize polymorphism to fetch combined posts
    all_posts = Post.objects.all().instance_of(Post)

    if search_query:
        all_posts = all_posts.filter(
            Q(title__icontains=search_query) | Q(
                description__icontains=search_query)
        )
    # Paginate the combined queryset
    paginated_posts = paginate_queryset(request, all_posts, items_per_page=10)
    search_url = reverse('posts:map_all_posts_view')
    google_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')

    context = {
        'posts': paginated_posts,
        'is_authenticated': request.user.is_authenticated,
        'active_tab': 'map',
        'items_per_page_options': ITEMS_PER_PAGE_OPTIONS,
        'search_query': search_query,
        'search_url': search_url,
        'GOOGLE_MAPS_API_KEY': google_api_key,
    }

    return render(request, 'view_all_posts_list.html', context)


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.user:
        messages.error(request,
                       "You do not have permission to delete this post.")
        return redirect('some_view_name')

    try:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting post: {e}")

    return HttpResponseRedirect(reverse('posts:view_all_posts'))
