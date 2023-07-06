from django.urls import path
from . import views
# from blog.views import Index

app_name = 'blog'

urlpatterns = [
    # path('', views.index), # FBV
    # path('', views.Index.as_view(), name='list'), # CBV
    # path('write/', views.write, name='write'),
    # 게시글
    path('', views.Index.as_view(), name='list'),
    path('write/', views.Write.as_view(), name='write'),
    path('detail/<int:post_id>/', views.DetailView.as_view(), name='detail'),
    path('detail/<int:post_id>/edit', views.Update.as_view(), name='edit'),
    path('detail/<int:post_id>/delete', views.Delete.as_view(), name='delete'),
    # # 코멘트
    path('detail/<int:post_id>/comment/write', views.CommentWrite.as_view(), name='cm-write'),
    path('detail/comment/<int:comment_id>/delete', views.CommentDelete.as_view(), name='cm-delete'),
    # # 태그
    # path('detail/<int:post_id>/tag/write', views.HashTagWrite.as_view(), name='tag-write'),
    # path('detail/tag/<int:hashTag_id>/delete', views.HashTagDelete.as_view(), name='tag-delete'),
]