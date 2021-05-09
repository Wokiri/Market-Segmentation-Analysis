from django.urls import path
from .views import (
    home_page_view,
    map_page_view,
    uploadExcel_view,
)

app_name = 'pages'

urlpatterns = [
    path('', home_page_view, name='home_page'),
    path('map/', map_page_view, name='map_page'),
    path('upload-file/', uploadExcel_view, name='upload_file_page'),
]
