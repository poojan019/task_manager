from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import CustomUser
from .models import Task
from .serializers import TaskSerializer

class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['MANAGER', 'ADMIN']
    
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Task.objects.all()
        if user.role == 'MANAGER':
            return Task.objects.filter(assigned_by=user)
        return Task.objects.filter(assigned_to=user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_permissions(self):
        if self.action in ['create', 'destroy', 'assign']:
            return [IsManagerOrAdmin()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        task = self.get_object()
        employee_id = request.data.get('employee_id')

        if not employee_id:
            return Response({'error': 'employee_id is required'}, status=400)

        try:
            employee = CustomUser.objects.get(id=employee_id, role='EMPLOYEE')
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid employee ID'}, status=400)
        
        task.assigned_to = employee
        task.save()
        return Response({'status': 'task assigned'})