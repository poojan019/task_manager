from rest_framework import serializers
from users.models import CustomUser
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='EMPLOYEE')
    )
    assigned_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_at', 'assigned_by', 'title', 'description', 'due_date', 'priority')

    def get_fields(self):
        fields = super().get_fields()
        user = self.context['request'].user

        if user.role == 'EMPLOYEE':
            for field in ['title', 'description', 'due_date', 'priority', 'assigned_to']:
                fields[field].read_only = True

        return fields

    def validate(self, data):
        user = self.context['request'].user
        instance = getattr(self, 'instance', None)

        # Creation validation
        if not instance and user.role not in ['MANAGER', 'ADMIN']:
            raise serializers.ValidationError("Only managers/admins can create tasks")
        
        # Update validation
        if instance and user.role == 'EMPLOYEE':
            if any(key != 'status' for key in data.key()):
                raise serializers.ValidationError("Employees can only update status")
            
        return data