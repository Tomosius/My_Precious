from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import LostPost, FoundPost
from .forms import LostPostForm, FoundPostForm, FileFieldForm
import os
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

ITEMS_PER_PAGE_OPTIONS = [5, 10, 20, 50]


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


def view_all_posts(request):
    lost_posts = LostPost.objects.all()
    found_posts = FoundPost.objects.all()
    all_posts = list(lost_posts) + list(found_posts)

    lost_photos = LostPhoto.objects.all()
    found_photos = FoundPhoto.objects.all()
    context = {
        'lost_posts': lost_posts,
        'found_posts': found_posts,
        'all_posts': all_posts,
    }

    return render(request, 'view_all_posts.html', context)



# Assuming your models have a 'user' field that links to the user who created the post
def post_detail_view(request, slug, post_type):

    google_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    model = LostPost if post_type == 'lost' else FoundPost
    post = get_object_or_404(model, slug=slug)

    # Check if the current user is the owner of the post
    is_owner = request.user == post.user

    PhotoModel = LostPhoto if post_type == 'lost' else FoundPhoto
    photos = PhotoModel.objects.filter(
        lost_post=post) if post_type == 'lost' else PhotoModel.objects.filter(
        found_post=post)

    return render(request, 'post_details.html', {
        'post_type': post_type,
        'post': post,
        'photos': photos,
        'is_owner': is_owner,  # Add 'is_owner' to the context
        'GOOGLE_MAPS_API_KEY': google_api_key
    })


def paginate_posts(request, posts_list, default_items_per_page=10):
    """
    Paginate posts for easier navigation, allowing dynamic items per page.
    """
    items_per_page = request.GET.get('items_per_page', default_items_per_page)
    try:
        items_per_page = int(items_per_page)
        if items_per_page <= 0:
            raise ValueError
    except ValueError:
        items_per_page = default_items_per_page

    paginator = Paginator(posts_list, items_per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)



def view_all_posts(request):
    """Display all posts, both lost and found."""
    lost_posts = LostPost.objects.all()
    found_posts = FoundPost.objects.all()
    all_posts = list(lost_posts) + list(found_posts)
    paginated_posts = paginate_posts(request, all_posts)
    is_authenticated = request.user.is_authenticated
    context = {'posts': paginated_posts, 'is_authenticated':
        is_authenticated, "active_tab": "all", "items_per_page_options": ITEMS_PER_PAGE_OPTIONS}
    return render(request, 'view_all_posts.html', context)



def view_lost_posts(request):
    """Display all lost posts."""
    lost_posts = LostPost.objects.all()
    paginated_posts = paginate_posts(request, lost_posts)
    is_authenticated = request.user.is_authenticated
    context = {'posts': paginated_posts, 'is_authenticated':
        is_authenticated, "active_tab": "lost", "items_per_page_options": ITEMS_PER_PAGE_OPTIONS}
    return render(request, 'view_all_posts.html', context)


def view_found_posts(request):
    """Display all found posts."""
    found_posts = FoundPost.objects.all()
    paginated_posts = paginate_posts(request, found_posts)
    is_authenticated = request.user.is_authenticated
    context = {'posts': paginated_posts, 'is_authenticated':
        is_authenticated, "active_tab": "found", "items_per_page_options": ITEMS_PER_PAGE_OPTIONS}
    return render(request, 'view_all_posts.html', context)





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
                photo_instance = photo_model_class(image=file, **{'lost_post': updated_post} if post_type == 'lost' else {'found_post': updated_post})
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

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import LostPhoto, FoundPhoto

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
# Ensure these imports are correct based on your app structure
from .models import LostPhoto, FoundPhoto

def delete_photo(request, photo_id, post_type):
    """
    Deletes a photo based on its ID and associated post type ('lost' or 'found').

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

    # Perform the deletion, which includes Cloudinary asset deletion via overridden delete method
    photo.delete()

    try:
        # Assuming the deletion code is here
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})




