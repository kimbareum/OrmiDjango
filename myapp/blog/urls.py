from django.urls import path
from . import views
# from blog.views import Index

urlpatterns = [
    # path('', views.index), # FBV
    path('', views.Index.as_view()) # CBV
]