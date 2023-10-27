from rest_framework import serializers


class GenericIdAndNameSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
