from rest_framework import serializers
from .models import Test_result


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_result
        fields = '__all__'
