from rest_framework import serializers

class SemesterFeeSerializer(serializers.Serializer):
    semester_id = serializers.IntegerField()
    year = serializers.IntegerField()
    term = serializers.CharField()
    total_fee = serializers.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    remaining_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
