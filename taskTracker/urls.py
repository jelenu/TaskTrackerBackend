from django.contrib import admin
from django.urls import path, include, re_path
from boards.views import ListBoardsView


urlpatterns = [
    # Admin routes
    path('admin/', admin.site.urls),

    path('boards/', ListBoardsView.as_view(), name='board-list'),


    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),


]