from django.contrib import messages
from django.shortcuts import render, redirect
from temple_app.models import MediaItem, Review


def index(request):
    error_message = None

    if request.method == "POST":
        form_type = request.POST.get('form_type')

        if form_type == 'review':
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            rating = request.POST.get('rating', '5')
            comment = request.POST.get('comment', '').strip()

            if not comment:
                error_message = 'Please enter a review or feedback message.'
            else:
                try:
                    rating_value = int(rating)
                except ValueError:
                    rating_value = 5
                Review.objects.create(
                    name=name,
                    email=email,
                    rating=rating_value,
                    comment=comment,
                )
                messages.success(request, 'Thank you! Your review has been saved.')
                return redirect('index')

        elif form_type == 'upload':
            if request.user.is_staff:
                for uploaded_file in request.FILES.getlist('files'):
                    MediaItem.objects.create(file=uploaded_file)
                messages.success(request, 'Your photo/video has been uploaded.')
            else:
                messages.error(request, 'Photo/video upload is restricted to site administrators.')
            return redirect('index')
        elif form_type == 'set_hero' and request.user.is_staff:
            media_id = request.POST.get('media_id')
            if media_id:
                MediaItem.objects.filter(is_hero=True).update(is_hero=False)
                MediaItem.objects.filter(pk=media_id, file__iendswith=('.jpg', '.jpeg', '.png', '.jfif', '.webp')).update(is_hero=True)
                messages.success(request, 'Hero image updated successfully.')
            return redirect('index')
        elif form_type == 'delete_media' and request.user.is_staff:
            media_id = request.POST.get('media_id')
            if media_id:
                MediaItem.objects.filter(pk=media_id).delete()
                messages.success(request, 'Media item deleted.')
            return redirect('index')

    media_items = MediaItem.objects.order_by('-uploaded_at')[:12]
    reviews = Review.objects.order_by('-created_at')[:8]

    hero_item = MediaItem.objects.filter(is_hero=True, file__iendswith=('.jpg', '.jpeg', '.png', '.jfif', '.webp')).order_by('-uploaded_at').first()

    hero_image = hero_item.file.url if hero_item else '/media/gopnath.jpg'
    return render(
        request,
        'index.html',
        {
            'media_items': media_items,
            'reviews': reviews,
            'hero_image': hero_image,
            'error_message': error_message,
        },
    )
