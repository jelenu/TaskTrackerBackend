# tasks/admin.py
from django.contrib import admin
from .models import Board, List, Card

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'creator')
    list_filter = ('creator',)
    search_fields = ('name',)

@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'board', 'order')
    list_filter = ('board',)
    search_fields = ('name',)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'list', 'order')
    list_filter = ('list',)
    search_fields = ('title', 'description')
