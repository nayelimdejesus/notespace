from django.urls import path
from . import views
from .views import JournalCreateView, JournalListView

urlpatterns = [
    path('', JournalListView.as_view(), name='journal'),
    path('new/', JournalCreateView.as_view(), name ='new_entry')
]
