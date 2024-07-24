from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import LoggingMixin


class HomeAPI(LoggingMixin, APIView):
    def post(self, request):
        return Response(data={'message': 'hello'}, status=status.HTTP_200_OK)
