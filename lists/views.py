from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from .models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    '''view of list'''
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    '''new list'''
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id):
    '''add item'''
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
