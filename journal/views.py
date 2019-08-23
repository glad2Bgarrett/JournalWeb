from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Entry
from .forms import EntryForm
from datetime import datetime


def dashboard(request):
    entries = Entry.objects.all().order_by('-created_date')[:5]
    todays = Entry.objects.filter(created_date__month=datetime.now().month, created_date__day=datetime.now().day)\
        .order_by('created_date')
    return render(request, 'journal/dashboard.html', {'entries': entries, 'todays': todays})


def entry_list_with_selected(request, pk):
    years_dict = get_entry_list()
    form = EntryForm()
    selected = Entry.objects.get(id=pk)
    return render(request, 'journal/entry_list.html', {'entries': years_dict, 'form': form, 'selected': selected})


def entry_list(request):
    years_dict = get_entry_list()
    form = EntryForm()
    return render(request, 'journal/entry_list.html', {'entries': years_dict, 'form': form})


def get_entry_list():
    entries = Entry.objects.all().order_by('-created_date')
    years_dict = dict()
    for entry in entries:
        month = entry.created_date.strftime("%B")
        if entry.created_date.year in years_dict:
            if month in years_dict[entry.created_date.year]:
                years_dict[entry.created_date.year][month].append(entry)
            else:
                years_dict[entry.created_date.year][month] = [entry]
        else:
            years_dict[entry.created_date.year] = {month: [entry]}
    return years_dict


def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if entry:
        entry.entry_was_read()
    json_entry = serializers.serialize('json', [entry])
    return JsonResponse({'entry': json_entry})


@csrf_exempt
def delete_entry(request, pk):
    entry = Entry.objects.get(id=pk)
    entry.delete()
    return HttpResponse(status=200)


def new_entry(request):
    if request.method == 'GET':
        form = EntryForm()
        return render(request, 'journal/edit_entry.html', {'form': form})
    elif request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
        return redirect('entry_list_with_selected', pk=entry.pk)


def edit_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'GET':
        form = EntryForm(instance=entry)
    elif request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save()
            return HttpResponse(status=200)
    return render(request, 'journal/edit_entry.html', {'form': form})
