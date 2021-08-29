from django.contrib import admin
from django.urls import path, include
from pytransfer import urls as ApiUrl
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='pyTransfer')


urlpatterns = [
    path('', schema_view, name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/', include(ApiUrl)),

]
