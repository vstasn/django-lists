from django.shortcuts import redirect, render
from .models import Item


def home_page(request):
    return render(request, 'home.html')


def view_list(request):
    '''view of list'''
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(request):
    '''new list'''
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/one-in-the-world-list/')
