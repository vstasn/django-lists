from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List


class ItemModelTest(TestCase):
    '''test item model'''

    def test_default_text(self):
        '''test: set default text'''
        item = Item()
        self.assertEqual(item.text, '')

class ListModelTest(TestCase):
    '''test: list model'''

    def test_get_absolute_url(self):
        '''test: get absolute url'''
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')


class ListAndItemModelsTest(TestCase):

    def test_item_is_related_to_list(self):
        '''test: item is related to list'''
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        '''test: can't add empty list items'''
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        '''test: duplicate items are invalid'''
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()
            # item.save()

    def test_CAN_save_same_items_to_different_lists(self):
        '''test: can save the same items to different lists'''
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  # should not raise

    def test_list_ordering(self):
        '''test: list ordering'''
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        '''test string representation'''
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')
