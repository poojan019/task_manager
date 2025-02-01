from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, CustomAuthToken, RoleUpdateView
from tasks.views import TaskViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('auth/register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('auth/login/', CustomAuthToken.as_view(), name='login'),
    path('users/<int:pk>/role/', RoleUpdateView.as_view(), name='user-role'),
    path('', include(router.urls)),
]
