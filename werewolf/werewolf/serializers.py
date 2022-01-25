from rest_framework import serializers

from werewolf.models import Game
from werewolf.models.actions import Vote


class GameSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField()

    class Meta:
        model = Game
        fields = ['owner', 'name', 'creation_date', 'start_date', 'end_date']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["who", "whom", "round"]
        read_only_fields = ["who", "round"]

    def validate(self, data):

        if data["whom"] == self.context["me"]:
            raise serializers.ValidationError('Cannot vote against itself')
        return data
