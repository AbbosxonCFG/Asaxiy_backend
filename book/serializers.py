from rest_framework import serializers 

from account.serializer import UserSerializer 
from .models import *


class AuthorSerialzier(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields=('id','name')


class BookSerializer(serializers.ModelSerializer):
    author=AuthorSerialzier()
    genre=serializers.SerializerMethodField()

    class Meta:
        model=Book
        fields=('id','author','genre','title', 'price')
        
    def get_genre(self,obj):
        data=[]
        for genre in obj.genre.all():
            data.append(
                {
                    'id':genre.id,
                    'name':genre.name
                }
            )
            return data

class BookPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=('id','author','genre','title', 'price')
        


    


class BookSerializerPk(serializers.ModelSerializer):
    author=AuthorSerialzier()
    genre=serializers.SerializerMethodField()
    tag=serializers.SerializerMethodField()
    class Meta:
        model=Book
        fields='__all__'
        
        depth=1

    def get_genre(self,obj):
        data=[]
        for genre in obj.genre.all():
            data.append(
                {
                    'id':genre.id,
                    'name':genre.name
                }
            )
            return data

    def get_tag(self,obj):
        data=[]
        for tag in obj.tag.all():
            data.append(
                {
                    'id':tag.id,
                    'name':tag.name
                }
            )
            return data
        
class FavoriteAuthorSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=FavoriteAuthor
        fields=('user',"author")
        depth=1

class FavoriteAuthorPostSerializer(serializers.ModelSerializer): 
    class Meta:
        model=FavoriteAuthor
        fields=('user',"author")
        # depth=1

class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feedback
        fields="__all__"
        depth=2