from django.contrib import admin
from django.urls import path, include
from authentication.views import Login, Logout
urlpatterns = [
    # Admin routes
    path('admin/', admin.site.urls),

    path('login/', Login.as_view(), name='login' ),
    path('logout/', Logout.as_view(), name='logout' ),

]