from django.shortcuts import render, HttpResponse
import json

# Create your views here.

def offline(request):
    return render(request, "offline.html")

def sw(request):
    return render(request, "service-worker.js", content_type="application/x-javascript")