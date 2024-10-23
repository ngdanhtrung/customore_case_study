from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    message = serializers.CharField()


class HealthCheckView(APIView):
    serializer_class = HealthCheckSerializer

    def get(self, request):
        serializer = self.serializer_class(data={"status": 200, "message": "OK"})
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
