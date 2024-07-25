from rest_framework.response import Response
from rest_framework.views import APIView

from tracking.mixins import LoggingMixin


class MockNoLoggingAPI(APIView):
    def get(self, request):
        return Response({'message': 'no logging'})


class MockLoggingAPI(LoggingMixin, APIView):
    def get(self, request):
        return Response({'message': 'logging'})
