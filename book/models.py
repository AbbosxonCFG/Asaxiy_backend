from django .db import models
from account .models import User



class Genre(models.Model):
    name = models.CharField(max_length=32)
    created_at=models.DateTimeField(auto_now_add=True)




class Tag(models.Model):
    name = models.CharField(max_length=32)
    created_at=models.DateTimeField(auto_now_add=True)




class Author(models.Model):
    name=models.CharField(max_length=32)
    avatar=models.ImageField(upload_to='avatar/')
    bio=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Book(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    author= models.ForeignKey(Author,on_delete=models.CASCADE)
    genre=models.ManyToManyField(Genre)
    tag=models.ManyToManyField(Tag, blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='books/', blank=True)

    def __str__(self):
        return self.title



class BookOrder(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    book=models.ForeignKey(Book, on_delete=models.CASCADE)
    status=models.CharField(max_length=32,default='going_to',choices=(
        ('going_to','going_to'),
        ('reading','reading' ),
        ('done','done'),
    ))
    is_paid=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)





class Feedback(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    raiting=models.IntegerField(default=0)
    text=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True) 



class WishList(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book.title



class FavoriteAuthor(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    author=models.ManyToManyField(Author , blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self): 
        return self.user.username




# class BookReaders(models.Model):
    # # user=models.ForeignKey(User, on_delete=models.CASCADE)
#     book=models.ForeignKey(Book, on_delete=models.CASCADE)
#     status=models.CharField(max_length=32,blank=True,null=True,choices=(
#         ('going_to','going_to'),
#         ('reading','reading' ),
#         ('done','done'),
#     ))

