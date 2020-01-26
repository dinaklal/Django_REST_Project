from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets,mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.forms.models import model_to_dict
from rest_framework.decorators import action
from rest_framework import renderers 
from rest_framework.generics import UpdateAPIView
from django.shortcuts import get_object_or_404
from test_api import serializers
from test_api import models
from test_api import permissions
from .models import film,UserProfile,Review




class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class =  serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)
    @action(detail=False)
    def recom_movies(self, request, *args, **kwargs):    
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        queryset = film.objects.all()
        serializer.is_valid()
        user = request.user
        print(user)
        if request.user.is_authenticated:
            recom = film.objects.filter(genre =user.favourite_genre ).values('name','release_date','genre')
            serializer = serializers.FilmSerializerInUserProfile(recom,many=True)   
            return Response(serializer.data)
        else:
            return Response("Please Log In to get recommended movies (Use token)",status=status.HTTP_400_BAD_REQUEST)

class updateFavGenre(UpdateAPIView):
    serializer_class =  serializers.UpFavSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.checkAuthentication,)  
  
    def put(self, request, pk, format=None):
        
        instance = UserProfile.objects.get(pk=pk)
        serializer  = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    #overridden post methodes to return user details
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        token, created = Token.objects.get_or_create(user=user)
        recom = film.objects.filter(genre =user.favourite_genre ).values('name','release_date','genre')
        serializer = serializers.FilmSerializerInUserProfile(recom,many=True)   
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'name':user.name,
            'email': user.email,
            'favourite_genre':user.favourite_genre,
            'recommended_movies':serializer.data
        })
    

class ReviewViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.all()
    permission_classes = (permissions.UpdateOwnReview, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user=self.request.user)



class filmViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.FilmSerializer
    permission_classes = (permissions.checkAuthentication,)

    queryset = models.film.objects.all()
    def perform_create(self, serializer):
        """sets upvote and downvotes to 0 at first"""
        serializer.save(upvotes=0,downvotes=0)
   
    
    @action(detail=False)
    def top_rated(self, request, *args, **kwargs):        
        queryset=models.film.objects.all().order_by('-upvotes')[:2]

        serializer = serializers.FilmSerializer(queryset,many=True)   
        return Response(serializer.data)
    
class upvote( APIView):
    serializer_class  = serializers.upSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.checkAuthentication,)  
    
    def put(self, request, pk, format=None):        
        instance = film.objects.get(pk=pk)
        instance.upvotes = instance.upvotes +1
        serializer  = serializers.upSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance.save()
        return Response(serializer.validated_data,status=status.HTTP_202_ACCEPTED)
class downvote( APIView):
    serializer_class  = serializers.upSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.checkAuthentication,)  
    
    def put(self, request, pk, format=None):        
        instance = film.objects.get(pk=pk)
        instance.downvotes = instance.downvotes +1
        serializer  = serializers.upSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance.save()
        return Response(serializer.validated_data,status=status.HTTP_202_ACCEPTED)