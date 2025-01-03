from rest_framework import serializers

class PullRequestSerializer(serializers.Serializer):
    title = serializers.CharField()
    url = serializers.URLField()
    state = serializers.CharField()
    created_at = serializers.DateTimeField()