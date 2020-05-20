from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from blog.decorators import ajax_required
from blog.forms import PhotoCreateForm
from blog.models import Photo


@login_required
def photo_create(request):
    if request.method == 'POST':
        form = PhotoCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Photo added successfully')
            return redirect(new_item.get_absolute_url())
        else:
            form = PhotoCreateForm(data=request.GET)
        return render(request, '', {'section': 'photos', 'form': form})


def photo_detail(request, id, slug):
    photo = get_object_or_404(Photo, id=id, slug=slug)
    return render(request,
                  'blog/photos/photo/detail.html',
                  {'section': 'photos',
                   'photo': photo})


@ajax_required
@login_required
@require_POST
def photo_like(request):
    photo_id = request.POST.get('id')
    action = request.POST.get('action')
    if photo_id and action:
        try:
            photo = Photo.objects.get(id=photo_id)
            if action == 'like':
                photo.users_like.add(request.user)
            else:
                photo.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})


@login_required
def image_list(request):
    photos = Photo.objects.all()
    paginator = Paginator(photos, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request,

                      'blog/photos/photo/list_ajax.html',

                      {'section': 'photos', 'photos': photos})

    return render(request,

                  'blog/photos/photo/list.html',

                  {'section': 'photos', 'photos': photos})
