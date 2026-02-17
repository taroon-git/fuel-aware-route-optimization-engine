from rest_framework import serializers


class RouteRequestSerializer(serializers.Serializer):
    start = serializers.CharField(required=True, max_length=255)
    end = serializers.CharField(required=True, max_length=255)
