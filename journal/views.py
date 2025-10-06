from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Entry
from .forms import EntryForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
MOOD_COLORS = {
    'happy': '#FFD700',
    'sad': '#1E90FF',
    'angry': '#FF4500',
    'anxious': '#8A2BE2',
    'neutral': '#A9A9A9',
    'excited': '#FF69B4',
    'relaxed': '#32CD32',
    'tired': '#808080',
    'confused': '#FFA500',
    'bored': '#C0C0C0',
    'love': '#FF1493',
    'in_love': '#FF69B4',
}

class JournalListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'journal/journal.html'
    context_object_name = 'entries'
    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user).order_by('-updated_at')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MOOD_COLORS'] = MOOD_COLORS
        return context
class EntriesListView(JournalListView):
    template_name = 'journal/view_all_entries.html'
    
class JournalCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    success_url = reverse_lazy('journal')
    form_class = EntryForm
    template_name = 'journal/entry_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class JournalDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = 'journal/entry_confirm_delete.html'
    success_url = reverse_lazy('journal')
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
class JournalUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = "journal/edit_entry.html"
    success_url = reverse_lazy("journal")

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)
    
@login_required
def view_entry(request, id):
    entry = get_object_or_404(Entry, id=id)
    
    return render(request, 'journal/view_entry.html', {'entry': entry})
    