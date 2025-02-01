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
        read_only_fields = ('created_date', 'assigned_by')

    def ceate(self, validated_data):
        validated_data['assigned_by'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        if self.context['request'].user.role == 'EMPLOYEE':
            if any(key != 'status' for key in data.keys()):
                raise serializers.ValidationError("Employees can only update status")
        return data