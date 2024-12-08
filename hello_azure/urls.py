from django.urls import path,re_path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name='hello_azure'
urlpatterns = [
    path('',views.index,name='index'),
    path('add/',views.add,name='add'),
    path('edit_item/', views.edit_item, name='edit_item'),
    path('update_item/', views.update_item, name='update_item'),
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('claim_item/',views.claim_item,name='claim_item'),
    path('items/', views.filtered_items, name='filtered_items'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)