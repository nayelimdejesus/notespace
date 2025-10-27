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
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

weeks = 53
days = 7

MOOD_COLORS = {
    'happy': (1.0, 0.843, 0.0),        
    'sad': (0.118, 0.565, 1.0),       
    'angry': (1.0, 0.271, 0.0),        
    'anxious': (0.541, 0.169, 0.886),  
    'neutral': (0.663, 0.663, 0.663),  
    'excited': (0.118, 1.0, 0.616),   
    'relaxed': (0.196, 0.804, 0.196),
    'tired': (0.502, 0.502, 0.502),    
    'confused': (1.0, 0.647, 0.0),    
    'bored': (0.753, 0.753, 0.753),    
    'love': (1.0, 0.082, 0.576),       
    'in_love': (1.0, 0.412, 0.706),   
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
        
        entries = self.get_queryset().order_by('updated_at')
        
        user_colors = []
        for entry in entries:
            color = MOOD_COLORS.get(entry.mood, (1.0, 1.0, 1.0)) 
            user_colors.append(color)

        grid_colors = []
        for week in range(weeks):
            week_colors = []
            for day in range(days):
                idx = week * days + day
                if idx < len(user_colors):
                    week_colors.append(user_colors[idx]) 
                else:
                    week_colors.append((1.0, 1.0, 1.0)) 
            grid_colors.append(week_colors)

        # Convert to 3D numpy array
        grid_colors = np.array(grid_colors, dtype=float)
        grid_colors = np.transpose(grid_colors, (1, 0, 2))

        fig, ax = plt.subplots(figsize=(16, 4))
        ax.imshow(grid_colors, aspect='equal')  # keep perfect squares

        # Draw visible grid lines manually (for all 53 weeks x 7 days)
        for x in range(weeks + 1):
            ax.axvline(x - 0.5, color='black', linewidth=0.4)
        for y in range(days + 1):
            ax.axhline(y - 0.5, color='black', linewidth=0.4)

        # Remove ticks but keep grid visible
        ax.set_xticks([])
        ax.set_yticks([])

        plt.tight_layout()


 
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig) 
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        context['mood_chart'] = f"data:image/png;base64,{image_base64}"

        
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
    