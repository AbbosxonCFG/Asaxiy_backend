from django.shortcuts import render
from rest_framework import status as rest_status
from rest_framework.decorators import api_view
from .models import *
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import permission_classes,authentication_classes
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from account.jwt_auth import JWTAuthentication
from account.permissions import IsAdmin
from rest_framework .authentication import TokenAuthentication


@api_view(['GET'])
# @authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def book_list(request):
    books=Book.objects.all()
    serializer=BookSerializer(books,many=True)
    # authors=request.GET.getlist('a_name')
    authors=request.GET.get('a_id')
    price1=request.GET.get('price_dan')
    price2=request.GET.get('price_gacha')
    words=request.GET.get('name')
    # genre=request.GET.get('genre')
    genre=request.GET.get('genre_id')
    if price1:
        books2=Book.objects.filter(price__gte=price1, price__lte=price2)
        serializer2=BookSerializer(books2, many=True)
        return Response(data=serializer2.data , status=200)
    
    if authors:
        # books=books.filter(author__name__in=authors)
        books3=books.filter(author__id__in=authors)
        serializer3=BookSerializer(books3,many=True)
        return Response(data=serializer3.data,status=200)
    
    if words:
        books4=books.filter(title__icontains=words)
        serializer4=BookSerializer(books4,many=True)
        return Response(data=serializer4.data,status=200)
    if genre:
        # books5=Book.objects.filter(genre__name__icontains=genre)
        books5=Book.objects.filter(genre__id__in=genre)
        serializer5=BookSerializer(books5,many=True)
        return Response(serializer5.data,status=200)
    
    contex={
        'massage':'list',
        'data':serializer.data
    }
    return Response(data=contex,status=rest_status.HTTP_200_OK)



'''
PK OLADI--------------------------------------------------------
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def book_pk(request,pk):
    try:
        book=Book.objects.get(id=pk)
        serializer=BookSerializerPk(book)
        return Response(data=serializer.data,status=200)
    except:
        return Response(data={'massage':'page not found'},status=404)



'''
POST-------------------------------------------------------------
'''


@api_view(['POST'])
@permission_classes([IsAdmin])
@authentication_classes([JWTAuthentication])
def book_post(request):
    data=request.data
    book=Book.objects.create( 
        title=data['titl'],
        description=data['description'],
        author_id=data['author_id'],
        # genre=data['genre'],
        image=data['image'],
        price=data['price']
    )
    return Response(data={'massage':'book created'},status=201)  




'''
PUT   AND    DELETE ---------------------------------------------------------
'''

@api_view(['DELETE','PUT'])
@permission_classes([IsAdmin])
@authentication_classes([JWTAuthentication])
def book_put_delete(request):
    if request.method == 'PUT':
        book_id = request.GET.get('id')
        title = request.data.get('title')
        description = request.data.get('description')
        price=request.data.get('price')
        # genre=request.data.get('genre')
        book = Book.objects.filter(id=book_id )
        if book.exists():
            book = book[0]
            if title is not None: book.title = title
            if description is not None: book.description = description
            if price is not None: book.price=price
            # if genre is not None: book.genre.id=genre
            book.save()
            return Response('book updated successfully!', status=rest_status.HTTP_200_OK)
        else: return Response({'ok': False}, status=rest_status.HTTP_404_NOT_FOUND)
    book_id = request.GET.get('id')
    if request.method=='DELETE':
        book = Book.objects.filter(id=book_id )
        if book.exists():
            book.delete()
            return Response({'massage':'book has been deleted'},status=200)
        else:
            return Response({'massage':'thomethings is wrong'},status=404)



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    try:
        user=request.user
        author_id=request.GET.get('author_id')
        author=Author.objects.get(pk=author_id)
        fav=FavoriteAuthor.objects.filter(user=user).first()
        if not fav:
            fav=FavoriteAuthor.objects.create(user=user)
        fav.author.add(author)
        fav.save()
        return Response({'massage':'book added succesfully'},status=201)
    except:
        return Response({'massage':'this user already excist'},status=rest_status.HTTP_400_BAD_REQUEST)
  
  


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_favorite(request):
    favorite=FavoriteAuthor.objects.filter(user=request.user).first()
    serializer=FavoriteAuthorSerializer(favorite)

    return Response(serializer.data, status=200)


@api_view(['POST'])
@authentication_classes([IsAuthenticated])
def order_book(request):
    user=request.user
    book_id=request.POST.get('book_id')
    is_paid=request.POST.get('is_paid')
    book=BookOrder.objects.filter(id=book_id)
    if book:
        return Response('Already ordered book')
    else:
        book=BookOrder.objects.create(
            user=user,
            book_id=book_id,
            status='want'

        )
        if is_paid or Book.objects.get(id=book_id).price==0:
            book.status='doing'
            book.is_paid=True
            book.save()
            return Response('Succesfully orderd book')
        else:
            return Response('Waiting payment')
    
    

    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_wishlist(request):
    # book_id=request.GET.get('book_id')
    pk=request.GET.get('pk')
    wishlist=WishList.objects.filter(book_id=pk)

    if not wishlist:
        WishList.objects.create(book_id=pk,user=request.user)
        return Response('created')
    else:
        wishlist[0].delete()
        return Response('deleted')
    



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def feedback(request):
    user=request.user
    book_id=request.POST.get("book_id")
    raiting=request.POST.get('raiting')
    text=request.POST.get('text')
    feedback_obj=Feedback.objects.create(
        user=user,
        book_id=book_id,
        raiting=raiting,
        text=text

    )

    serializer=FeedBackSerializer(feedback_obj)

    return Response(serializer.data,status=201)
    

@api_view(['GET'])
def get_feedback(request):
    book_id=request.GET.get('book_id')
    feedback=Feedback.objects.filter(book_id=book_id)
    serializer=FeedBackSerializer(feedback,many=True)
    return Response(serializer.data,status=200)



























