from .models import*
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.response import Response
from account.jwt_auth import JWTAuthentication
from account.permissions import IsAdmin


class BookList(ListAPIView):
    queryset=Book.objects.all().order_by('-id')
    serializer_class=BookSerializer

    def get_queryset(self):
        books=Book.objects.all()
        # authors=request.GET.getlist('a_name')
        authors=self.request.GET.get('a_id')
        price1=self.request.GET.get('price_dan')
        price2=self.request.GET.get('price_gacha')
        words=self.request.GET.get('name')
        # genre=request.GET.get('genre')
        genre=self.request.GET.get('genre_id')
        if price1:
            books=Book.objects.filter(price__gte=price1, price__lte=price2)
            
        if authors:
            # books=books.filter(author__name__in=authors)
            books=books.filter(author__id__in=authors)
           
        if words:
            books=books.filter(title__icontains=words)
            
        if genre:
            # books5=Book.objects.filter(genre__name__icontains=genre)
            books=Book.objects.filter(genre__id__in=genre)
        
        return books



class BookDetail(RetrieveAPIView):
    serializer_class=BookSerializerPk
    queryset=Book.objects.all()



class BookAdd(CreateAPIView):
    permission_classes = (IsAdmin,)
    authentication_classes = (JWTAuthentication,)
    serializer_class=BookPostSerializer

    
 



class BookDelete(DestroyAPIView):
    permission_classes = (IsAdmin,)
    authentication_classes = (JWTAuthentication,)
    serializer_class=BookSerializer
    



class AddFavorite(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class=FavoriteAuthorPostSerializer  
    queryset=Book.objects.all()
    def create(self, request, *args, **kwargs):
        user=request.user
        data=request.data.dict()
        data['user']=user.id
        print(data)
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'massage':'ok'})
        
        else:
            return Response(serializer.errors,status=400)
        



class GetFavorite(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class=FavoriteAuthorSerializer
    def get_queryset(self):
        queryset=FavoriteAuthor.objects.filter(user=self.request.user)
        return queryset
    

def git (request):
    book=Book.objects.all()
    serializer=BookSerializer(book,many=True)
    return Response(serializer.data)