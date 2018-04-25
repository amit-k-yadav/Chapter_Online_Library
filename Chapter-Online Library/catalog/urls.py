from django.conf.urls import url
from catalog import views
# from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)/$', views.BookDetailsView.as_view(), name='book-details'),
    url(r'^authors/$', views.AuthorsListView.as_view(), name='authors'),
    url(r'^author/(?P<pk>\d+)/$', views.AuthorsDetailView.as_view(), name='author-details'),
    url(r'^my_books/$', views.MyBooksListView.as_view(), name='my_books'),
    url(r'^all_borrowed/$',views.all_borrowed_books, name='all_borrowed'),
    url(r'^add_book/$', views.add_book, name='add_book'),
    url(r'^renew/(?P<pk>[\w\-]+)/$', views.renew , name='renew'),
    url(r'authors/create/$', views.AuthorCreate.as_view(), name='add-author'),
    url(r'authors/update/(?P<pk>\d+)/$', views.AuthorUpdate.as_view(), name='update-author'),
    url(r'authors/delete/(?P<pk>\d+)/$', views.AuthorDelete.as_view(), name='delete-author'),
    url(r'pdf/(?P<pk>\d+)/$', views.pdf_generation, name='pdf'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>.+)/(?P<token>.+)/$',views.activate, name='activate'),
    url(r'^available_books/$',views.available_books, name='available_books'),
    url(r'^borrow/(?P<pk>.+)/(?P<user_pk>.+)/$', views.borrow_book, name='borrow_book')
#     #Youtube
#     url(r'^password_reset/$', password_reset, name='password_reset'),
#     url(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),
#     url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name='password_reset_confirm'),
#     url(r'^password_reset_complete/$', password_reset_complete, name='password_reset_complete'),

]
