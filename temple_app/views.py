from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from temple_app.models import MediaItem, Review, VisitorLog


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        "Sitemap: https://gopnath-temple.onrender.com/sitemap.xml\n"
    )
    return HttpResponse(content, content_type="text/plain")



def index(request):
    error_message = None

    # Track visitor count
    if not request.session.session_key:
        try:
            request.session.save()
        except Exception:
            pass
    session_key = request.session.session_key or ""
    client_ip = get_client_ip(request)

    total_visits = 0
    unique_visitors = 0

    if request.method == "GET":
        try:
            # Check if this IP address OR session key has EVER been logged
            already_logged = False
            if client_ip:
                already_logged = VisitorLog.objects.filter(ip_address=client_ip).exists()
            if not already_logged and session_key:
                already_logged = VisitorLog.objects.filter(session_key=session_key).exists()

            if not already_logged:
                VisitorLog.objects.create(ip_address=client_ip, session_key=session_key)

            total_visits = VisitorLog.objects.count()
            unique_visitors = total_visits
        except Exception:
            total_visits = 1
            unique_visitors = 1



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
            'total_visits': total_visits,
            'unique_visitors': unique_visitors,
        },
    )

