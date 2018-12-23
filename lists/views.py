from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from .forms import ExistingListItemForm, ItemForm
from .models import Item, List

User = get_user_model()


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    '''view of list'''
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)

    return render(request, 'list.html', {'list': list_, 'form': form})


def new_list(request):
    '''new list'''
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List()
        list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})


def my_lists(request, email):
    '''my lists'''
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})
