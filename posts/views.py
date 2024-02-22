import os
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import LostPostForm, FoundPostForm, FileFieldForm
from .models import LostPost, FoundPost, LostPhoto, FoundPhoto
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import LostPost, FoundPost, Post  # Assuming you have a third
from django.urls import reverse


@login_required
def create_post(request):
    google_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    post_type = request.POST.get('post_type')
    form_class = LostPostForm if post_type == 'lost' else FoundPostForm

    if request.method == 'POST':
        form = form_class(request.POST)
        image_form = FileFieldForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            post_instance = form.save(commit=False)
            post_instance.user = request.user
            post_instance.save()

            if post_type == 'lost':
                photo_model_class = LostPhoto
                photo_kwargs = {'lost_post': post_instance}
            else:  # post_type == 'found'
                photo_model_class = FoundPhoto
                photo_kwargs = {'found_post': post_instance}

            for file in request.FILES.getlist('file_field'):
                photo_instance = photo_model_class(image=file, caption='',
                                                   **photo_kwargs)
                photo_instance.save()

            return redirect('/')
        else:
            print(form.errors)

    else:
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

from django.shortcuts import render
from .models import Post  # Assuming Post is the polymorphic base model
from django.core.paginator import Paginator

ITEMS_PER_PAGE_OPTIONS = [5, 10, 20, 50]

def paginate_queryset(request, queryset, items_per_page=10):
    """
    Paginate a queryset and return the page object for the current request.
    """
    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def view_all_posts(request):
    """
    Display all posts (both LostPost and FoundPost) with optional search functionality and pagination,
    utilizing Django Polymorphic for combined querying.
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
    search_url = reverse('posts:view_all_posts')

    context = {
        'posts': paginated_posts,
        'is_authenticated': request.user.is_authenticated,
        'active_tab': 'all',
        'items_per_page_options': ITEMS_PER_PAGE_OPTIONS,
        'search_query': search_query,
        'search_url': search_url,
    }

    return render(request, 'view_all_posts.html', context)


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
    return render(request, 'view_all_posts.html', context)

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
    return render(request, 'view_all_posts.html', context)




def post_detail_view(request, slug, post_type):
    google_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    model = LostPost if post_type == 'lost' else FoundPost
    post = get_object_or_404(model, slug=slug)

    # Check if the current user is the owner of the post
    is_owner = request.user == post.user

    photo_model = LostPhoto if post_type == 'lost' else FoundPhoto
    photos = photo_model.objects.filter(
        lost_post=post) if post_type == 'lost' else photo_model.objects.filter(
        found_post=post)

    return render(request, 'post_details.html', {
        'post_type': post_type,
        'post': post,
        'photos': photos,
        'is_owner': is_owner,  # Add 'is_owner' to the context
        'GOOGLE_MAPS_API_KEY': google_api_key
    })


@login_required
def update_post(request, slug, post_type):
    model = LostPost if post_type == 'lost' else FoundPost
    post = get_object_or_404(model, slug=slug)
    # Check if the current user is the owner of the post

    PhotoModel = LostPhoto if post_type == 'lost' else FoundPhoto
    photos = PhotoModel.objects.filter(
        lost_post=post) if post_type == 'lost' else PhotoModel.objects.filter(
        found_post=post)

    google_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    form_class = LostPostForm if post_type == 'lost' else FoundPostForm
    model_class = LostPost if post_type == 'lost' else FoundPost
    photo_model_class = LostPhoto if post_type == 'lost' else FoundPhoto

    post_instance = get_object_or_404(model_class, slug=slug, user=request.user)

    # Check if the current user is the owner of the post
    is_owner = request.user == post.user

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=post_instance)
        image_form = FileFieldForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            updated_post = form.save()

            for file in request.FILES.getlist('file_field'):
                photo_instance = photo_model_class(image=file, **{
                    'lost_post': updated_post} if post_type == 'lost' else {
                    'found_post': updated_post})
                photo_instance.save()

            return render(request, 'post_details.html', {
                'post_type': post_type,
                'post': post,
                'photos': photos,
                'is_owner': is_owner,  # Add 'is_owner' to the context
                'GOOGLE_MAPS_API_KEY': google_api_key
            })
        else:
            print(form.errors)
    else:
        form = form_class(instance=post_instance)
        image_form = FileFieldForm()

    return render(request, 'update_post.html', {
        'photos': photos,
        'form': form,
        'image_form': image_form,
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
        post_slug = photo.lost_post.slug
    elif post_type == 'found':
        photo = get_object_or_404(FoundPhoto, pk=photo_id)
        post_slug = photo.found_post.slug
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
    Display all posts (both LostPost and FoundPost) with optional search functionality and pagination,
    utilizing Django Polymorphic for combined querying.
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

    return render(request, 'view_all_posts.html', context)


