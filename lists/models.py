from django.db import models


class Item(models.Model):
    '''element of list'''
    text = models.TextField(default='')
