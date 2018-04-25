from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Book, Genre, Language, Author, BookInstance
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RenewForm, AddBooksForm, BorrowBookForm
from django.urls import reverse
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from weasyprint import HTML, CSS
from django.template.loader import get_template, render_to_string
#image file in weasyprint
from django.conf import settings


#email
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import base64

def index(request):
    num_books = Book.objects.all().count()
    num_book_instances = BookInstance.objects.all().count()
    available_books = BookInstance.objects.filter(status = 'A').count()
    num_authors = Author.objects.count()
    num_genre = Genre.objects.filter(name__icontains='cti').count()
    #Sessions
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return render(request, 'catalog/index.html', {'num_books':num_books, 'available_books':available_books,
                                                 'num_book_instances':num_book_instances, 'num_authors':num_authors,
                                                 'num_genre':num_genre, 'num_visits':num_visits})

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'
    paginate_by = 4
    #queryset = Book.objects.all()
    '''
    def get_context_data(self, **kwargs): #Using this we can add more context variables
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context
    '''


class BookDetailsView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_details.html'
    #query_set = Book.objects.get(pk=pk)
    context_object_name = 'book_list'
'''
    def get_context_data(self, **kwargs): #Using this we can add more context variables
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context
'''
'''
def book_detail_view(request,pk):
    try:
        book_list=Book.objects.get(pk=pk)
        book_instance=BookInstance.objects.filter(book=book_list)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    return render(
        request,
        'catalog/book_details.html',
        context={'book_list':book_list,'book_instance':book_instance}
    )
'''
class AuthorsListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    paginate_by = 4
    template_name = 'catalog/author_list.html'


class AuthorsDetailView(generic.DetailView):
    model =Author
    template_name = 'catalog/author_details.html'
    context_object_name = 'authors_detail'
'''
def authors_detail_view(request, pk):
    try:
        authors_detail = Author.objects.get(pk=pk)
        books_written = Book.objects.filter(authors=authors_detail)
    except Author.DoesNotExist:
        raise Http404("Author does not exist")
    return render(request, 'catalog/author_details.html', {'authors_detail':authors_detail,
                                                          'books_written':books_written})
'''

#list of books borrowed by the user
class MyBooksListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    context_object_name = 'my_books'
    login_url = '/login/'
    paginate_by = 4
    template_name = 'catalog/my_books.html'
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status='O')

@staff_member_required(login_url='/login/')
def all_borrowed_books(request):
    all_borrowed = BookInstance.objects.filter(status='O')
    return render(request, 'catalog/all_borrowed_books.html', {'all_borrowed':all_borrowed})



@staff_member_required(login_url='/login/')
def add_book(request):
    if request.method=='POST':
        form = AddBooksForm(request.POST)
        if form.is_valid:
            form.save(commit=True)
            return HttpResponseRedirect(reverse('books'))
        else:
            print(form.errors)
    else:
        form = AddBooksForm()
    return render(request, 'catalog/add_book.html', {'form':form})

@staff_member_required(login_url='/login/')
def renew(request, pk):
    book_inst = BookInstance.objects.get(pk=pk)
    if request.method == 'POST':
        form = RenewForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renew_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('all_borrowed'))
        else:
            print (form.errors)
    else:
        proposed_new_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewForm(initial={'renew_date':proposed_new_date,})
    return render(request, 'catalog/renew_book.html', {'form':form})


class AuthorCreate(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = Author
    fields = '__all__'
    template_name_suffix = '_add_form' #template name will be 'author_add_form'

class AuthorUpdate(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = Author
    fields = '__all__'
    template_name_suffix = '_add_form'

class AuthorDelete(LoginRequiredMixin,DeleteView):
    login_url = '/login/'
    model = Author
    success_url = reverse_lazy('authors')

def pdf_generation(request, pk):
    #html_template = get_template('catalog/home_page.html')
    book = Book.objects.get(pk=pk)
    html_template = render_to_string('catalog/pdf_file.html',{'book':book})
    pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="home_page.pdf"'
    return response


#email
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('catalog/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                #'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'uid': (str(user.pk*12)+str(549)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('<strong>We have sent a link to the entered email address. Please click on the link to verify and activate your account.</strong>')
    else:
        form = SignupForm()
    return render(request, 'catalog/signup.html', {'form': form})

#email activate
def activate(request, uidb64, token):
    try:
        uid = int(int(uidb64[:-3])/12)
        #uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account. ')
    else:
        return HttpResponse('Activation link is invalid!')


def available_books(request):
    books_available = BookInstance.objects.filter(status='A')
    return render(request, 'catalog/available_books.html',{'books_available':books_available})

def borrow_book(request, pk, user_pk):
    bk_inst = BookInstance.objects.get(pk=pk)
    user = User.objects.get(pk=user_pk)
    if request.method == "POST":
        form = BorrowBookForm(request.POST)
        if form.is_valid():
            bk_inst.due_back = form.cleaned_data['due_back']
            bk_inst.status = 'O'
            bk_inst.borrower = user
            bk_inst.save()
            return HttpResponseRedirect(reverse('available_books'))
        else:
            print(form.errors)
    else:
        form = BorrowBookForm()
    return render(request, 'catalog/borrow_book.html', {'form':form})
