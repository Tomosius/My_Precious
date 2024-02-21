import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LostPostForm, FoundPostForm, FileFieldForm
from .models import LostPhoto, FoundPhoto, LostPost, FoundPost
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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


def post_detail_view(request, slug, post_type):
    google_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    model = LostPost if post_type == 'lost' else FoundPost
    post = get_object_or_404(model, slug=slug)

    PhotoModel = LostPhoto if post_type == 'lost' else FoundPhoto
    photos = PhotoModel.objects.filter(
        lost_post=post) if post_type == 'lost' else PhotoModel.objects.filter(
        found_post=post)

    return render(request, 'post_details.html', {
        'post': post,
        'photos': photos,
        'GOOGLE_MAPS_API_KEY': google_api_key
    })


def paginate_posts(request, posts_list):
    """Paginate posts for easier navigation."""
    paginator = Paginator(posts_list, 10)  # Display 10 posts per page
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
        is_authenticated, "active_tab": "all"}
    return render(request, 'view_all_posts.html', context)


def view_lost_posts(request):
    """Display all lost posts."""
    lost_posts = LostPost.objects.all()
    paginated_posts = paginate_posts(request, lost_posts)
    is_authenticated = request.user.is_authenticated
    context = {'posts': paginated_posts, 'is_authenticated':
        is_authenticated, "active_tab": "lost"}
    return render(request, 'view_all_posts.html', context)


def view_found_posts(request):
    """Display all found posts."""
    found_posts = FoundPost.objects.all()
    paginated_posts = paginate_posts(request, found_posts)
    is_authenticated = request.user.is_authenticated
    context = {'posts': paginated_posts, 'is_authenticated':
        is_authenticated, "active_tab": "found"}
    return render(request, 'view_all_posts.html', context)
