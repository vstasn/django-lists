from django.shortcuts import redirect, render
from .models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request):
    '''view of list'''
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(request):
    '''new list'''
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/one-in-the-world-list/')
