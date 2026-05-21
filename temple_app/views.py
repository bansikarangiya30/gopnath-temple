from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

# Create your views here.

def index(request):
    uploaded_urls = request.session.pop('uploaded_urls', [])

    if request.method == "POST" and request.FILES.getlist("files"):
        fs = FileSystemStorage()
        uploaded_urls = []
        for uploaded_file in request.FILES.getlist("files"):
            filename = fs.save(uploaded_file.name, uploaded_file)
            uploaded_urls.append(fs.url(filename))
        request.session['uploaded_urls'] = uploaded_urls
        return redirect('index')

    return render(request, "index.html", {"uploaded_urls": uploaded_urls})