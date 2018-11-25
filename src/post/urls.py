from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = "posts"

router = DefaultRouter()
router.register(r"(?P<post_id>.+)/comments", views.PostCommentViewSet, basename="post-comment")
# router.register("m/<str:username>", views.UserViewSet)

urlpatterns = [
    path("", views.PostCreateView.as_view()),
    path("<uuid:id>", views.PostView.as_view(), name="post-detail"),
    path("feed", views.FeedView.as_view()),
    # path("<uuid:id>/comments", views.PostCommentView.as_view(), name="post-comment"),
    path("<uuid:id>/likes", views.PostLikeView.as_view(), name="post-like"),
    path("", include(router.urls)),
]
