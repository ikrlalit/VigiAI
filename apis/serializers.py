from rest_framework import serializers

class AddEvent_s(serializers.Serializer):
    source_name = serializers.CharField(required=True)
    event_type = serializers.CharField(required=True)
    severity = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    class Meta:
        fields='__all__'
class AddNewUser_s(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    role = serializers.CharField(required=True)
    class Meta:
        fields='__all__'
class AlertsList_s(serializers.Serializer):
    event_severity = serializers.CharField(required=False, allow_blank=True, default=None)
    alert_status = serializers.CharField(required=False,allow_blank=True, default=None)


    class Meta:
        fields='__all__'
class AlertStatusUpdate_s(serializers.Serializer):
    alert_id = serializers.IntegerField(required=True)
    alert_status = serializers.CharField(required=False,allow_blank=True, default=None)


    class Meta:
        fields='__all__'