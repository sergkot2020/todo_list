from django.shortcuts import render, reverse, redirect
from list_item.models import ListItem
from main.models import ListModel
from list_item.forms import ListItemForm
from django.http import HttpResponseNotFound, HttpResponse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from todo_list_ngu.settings import PAGE_COUNT
from django.contrib.auth.decorators import login_required
import json


@login_required(login_url='registration/login/')
def list_item_view(request, pk):
    user = request.user
    list_items = ListItem.objects.filter(
        list=pk, list__user=user).order_by('created')

    paginator = Paginator(list_items, PAGE_COUNT)
    page = request.GET.get('page', 1)
    try:
        list_page = paginator.page(page)
    except PageNotAnInteger:
        list_page = paginator.page(1)
    except EmptyPage:
        list_page = paginator.page(paginator.num_pages)

    list_name = ListModel.objects.filter(id=pk).first()
    context = {
        'list_items': list_page,
        'user': user.username,
        'list_name': list_name,
        'pages': list(paginator.page_range),
        'page_count_js': json.dumps(len(paginator.page_range)),
        'items_count_js': json.dumps(list_items.count()),
        'current_page': json.dumps(page),
        'item_on_page': json.dumps(len(list_page)),
        'max_item_on_page': json.dumps(PAGE_COUNT)
    }
    return render(request, 'list.html', context)


@login_required(login_url='registration/login/')
def create_item_view(request, pk):
    form = ListItemForm()
    if request.method == 'POST':
        name = request.POST['name']
        expire_date = request.POST['expire_date']
        form = ListItemForm({
            'name': name,
            'expire_date': expire_date,
            'list': pk
        })
        success_url = reverse('list_item:list_item', kwargs={'pk': pk})

        if form.is_valid():
            form.save()
            return redirect(success_url)

    return render(
        request, 'new_list_item.html', {'form': form, 'pk': pk}
    )


@login_required(login_url='registration/login/')
def edit_list_item_view(request, pk):
    list_item = ListItem.objects.filter(id=pk).first()
    list_id = list_item.list_id

    if request.method == 'POST':
        form = ListItemForm({
            'name': request.POST['name'],
            'expire_date': request.POST['expire_date'],
            'list': list_id
        }, instance=list_item)
        success_url = reverse('list_item:list_item', kwargs={'pk': list_id})

        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = ListItemForm(instance=list_item)

    return render(
        request, 'edit_list_item.html', {'form': form, 'pk': list_id}
    )


@login_required(login_url='registration/login/')
def done_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        pk = int(data['id'])
        list_item = ListItem.objects.get(id=pk)
        value = not list_item.is_done
        list_item.is_done = value
        list_item.save()
        return HttpResponse(status=201)
    return HttpResponse(status=404)


@login_required(login_url='/registration/login/')
def delete_item_view(request, pk):
    if request.method == 'POST':
        list_item = ListItem.objects.filter(id=pk).first()
        if list_item:
            list_item.delete()
            return HttpResponse(status=201)

    return HttpResponse(status=404)


def all_done_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        all_true, list_id = data.get('all_true'), data.get('list_id')
        value = not all_true
        if list_id:
            list_ = ListModel.objects.get(id=list_id)
            list_.listitem_set.all().update(is_done=value)
            list_.is_done = value
            list_.save()
            return HttpResponse(status=201)
    return HttpResponse(status=404)
