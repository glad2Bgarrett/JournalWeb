from django.shortcuts import render, get_object_or_404, redirect
from .models import Entry
from .forms import EntryForm
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


def new_entry(request):
    if request.method == 'GET':
        form = EntryForm()
        return render(request, 'journal/edit_entry.html', {'form': form})
    elif request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
        return redirect(request, 'journal/entry_detail.html', pk=entry.pk)


def edit_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'GET':
        form = EntryForm(instance=entry)
    elif request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save()
            return redirect('entry_detail', pk=entry.pk)
    return render(request, 'journal/edit_entry.html', {'form': form})
