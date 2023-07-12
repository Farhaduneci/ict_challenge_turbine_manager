from rest_framework import serializers

from .constants import CommandChoices


class CommandSerializer(serializers.Serializer):
    command = serializers.ChoiceField(choices=CommandChoices.choices)
