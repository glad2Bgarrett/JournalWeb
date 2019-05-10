from django.shortcuts import render, get_object_or_404
from .models import Entry
from datetime import datetime


def entry_list(request):
    entries = Entry.objects.all().order_by('-created_date')[:5]
    todays = Entry.objects.filter(created_date__month=datetime.now().month, created_date__day=datetime.now().day)\
        .order_by('created_date')
    return render(request, 'journal/entry_list.html', {'entries': entries, 'todays': todays})


def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if entry:
        entry.entry_was_read()
    return render(request, 'journal/entry_detail.html', {'entry': entry})
