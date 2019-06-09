from rest_framework import serializers
from .models import StudentPlan


class StudentPlanSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = StudentPlan
        fields = ('id', 'curriculum', 'max_credits')