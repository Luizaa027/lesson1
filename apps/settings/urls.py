from django import path 
from apps.settings.views import HelloView   

urlpattens = [
    path('hello/', HelloView.as_view(), name='hello'),
]   