from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Test_result
from django.http import JsonResponse
from .serializers import TestResultSerializer

class TestResultDetail(APIView):

    def get(self, request, id_number):
        try:
            test = Test_result.objects.get(id_number=id_number)
            serializer = TestResultSerializer(test)
            return Response(serializer.data)
        except:
            return Response({'error': 'Not found'}, status=404)
