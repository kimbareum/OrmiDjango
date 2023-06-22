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
    path('detail/<int:post_id>/', views.DetailView.as_view(), name='detail'),
    path('detail/<int:pk>/edit', views.Update.as_view(), name='edit'),
    path('detail/<int:pk>/delete', views.Delete.as_view(), name='delete'),
    # 코멘트
    path('detail/<int:post_id>/comment', views.CommentWrite.as_view(), name='comment'),
]