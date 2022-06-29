# accounts/serializers.py
from rest_framework import serializers
from datetime import datetime
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
      
class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    current_date = serializers.SerializerMethodField()
      
    @extend_schema_field(OpenApiTypes.DATETIME)
    def get_current_date(self, obj):
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        return date_time