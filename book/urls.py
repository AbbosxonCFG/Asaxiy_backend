from django . urls import path
from .views import *
from .class_views import *
from rest_framework.authtoken .views import obtain_auth_token

urlpatterns=[
    path('list/',book_list),
    path('list/<int:pk>/',book_pk),
    path('book_post/',book_post),
    path('book_put_delete/',book_put_delete),
    path('add_favorite/',add_favorite),
    path('get_favorite/',get_favorite),
    path('wishlist/',book_wishlist),
    path('feedback/',feedback),
    path('feedbacks/',get_feedback),


    # path ('list/',BookList.as_view()),
    # path ('book<int:pk>/',BookDetail.as_view()),
    # path ('book/add/',BookAdd.as_view()),
    # path ('book/delete/<int:pk>/',BookDelete.as_view()),
    # path ('getfavorite',GetFavorite.as_view()),
    # path ('addfavorite/',AddFavorite.as_view()),
    # # path('<int:pk>/',book_pk),
    # path('list/',book_list_pk)

]