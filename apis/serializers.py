from rest_framework import serializers

class AddEvent_s(serializers.Serializer):
    source_name = serializers.CharField(required=True)
    event_type = serializers.CharField(required=True)
    severity = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        fields='__all__'