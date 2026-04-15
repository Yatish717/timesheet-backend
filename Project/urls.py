from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from account import views

@csrf_exempt
def health(request):
    return HttpResponse("OK")

urlpatterns = [
    path('health/', health),
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('user/', include('account.urls')),
    path('project/', include('projectdata.urls')),
    path('timesheet/', include('timesheet.urls')),
    path('tracker/', include('tracker.urls')),
]