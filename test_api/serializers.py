from rest_framework import serializers

from test_api import models
from .models import UserProfile,film



class UpFavSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('favourite_genre',)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password','favourite_genre')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user


class ReviewSerializer(serializers.ModelSerializer):
    """Serializes review"""

    class Meta:
        model = models.Review
        fields = ('id', 'user', 'review_text','film', 'created_on')
        extra_kwargs = {'user': {'read_only': True}}
class FilmSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.film
        fields = ('id', 'name', 'release_date', 'genre','upvotes','downvotes')
        extra_kwargs = {
            'upvotes': {'read_only': True},
            'downvotes': {'read_only': True}
        }
   
class FilmSerializerInUserProfile(serializers.ModelSerializer):
    """Serializes film"""

    class Meta:
        model = models.film
        fields = ('name', 'release_date', 'genre')
class upSerializer(serializers.Serializer):
    def validate(self, data):
        return data

    
    
