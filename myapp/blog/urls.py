from django.urls import path
from . import views
# from blog.views import Index

app_name = 'blog'

urlpatterns = [
    # path('', views.index), # FBV
    # path('', views.Index.as_view(), name='list'), # CBV
    # path('write/', views.write, name='write'),
    # 제네릭뷰
    path('', views.List.as_view(), name='list'),
    path('write/', views.Write.as_view(), name='write'),
    path('detail/<int:pk>/', views.Detail.as_view(), name='detail'),
]