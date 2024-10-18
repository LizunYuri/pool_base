from django.http import JsonResponse
import json
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


def panel(request):
    return render(request, 'pages/panel.html')

def accountant_panel(request):
    return render(request, 'pages/accountant_panel.html')
