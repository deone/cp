from django.urls import path
from django.views.generic import TemplateView

app_name = 'transaction'
urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
]