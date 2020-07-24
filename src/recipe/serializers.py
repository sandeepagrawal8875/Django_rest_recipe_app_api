from rest_framework import serializers

from core.models import Tag, Ingredient

class TagSerializer(serializers.ModelSerializer):
    """Seralizer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id','name')
        read_only_field = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """serializers for Ingredients objests"""
    class Meta:
        model = Ingredient
        fields = ('id','name')
        read_only_fields = ('id',)