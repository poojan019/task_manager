from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsManagerOrAdmin, IsTaskAssigneeOrAdmin

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'description']
    ordering = ['-created_date']

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.all().order_by('-created_date')

        if user.role == 'ADMIN':
            return Task.objects.all()
        if user.role == 'MANAGER':
            return Task.objects.filter(assigned_by=user)
        
        return Task.objects.filter(assigned_to=user)
    
    def get_permissions(self):
        if self.action in ['create']:
            return [IsManagerOrAdmin()]
        if self.action in ['update', 'partial_update']:
            return [IsTaskAssigneeOrAdmin()]
        if self.action in ['destroy']:
            return [permissions.IsAdminUser()]
        
        return []
    
    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)
