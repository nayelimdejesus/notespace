from django.urls import path
from . import views
from .views import JournalCreateView, JournalListView, JournalUpdateView, EntriesListView, JournalDeleteView

urlpatterns = [
    path('', JournalListView.as_view(), name='journal'),
    path('new/', JournalCreateView.as_view(), name ='new_entry'),
    path('entries/', EntriesListView.as_view(), name='entries'),
    path('entry/<int:id>/', views.view_entry, name='view_entry'),
    path('entry/<int:pk>/delete/', JournalDeleteView.as_view(), name='entry_delete'),
    path("entry/<int:pk>/edit/", JournalUpdateView.as_view(), name="edit_entry"),]
