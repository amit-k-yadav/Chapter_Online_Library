from django.db import models
import uuid
from django.urls import reverse
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter the book genre (e.g Science Fiction, Romantic, Drama)")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200, help_text="Name of the book", blank=False)
    authors = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre,help_text="Genre of the book", blank=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book", null=True, blank=True)
    #imprint = models.TextField(blank=True, null=True, help_text="Imprint of the book")
    isbn = models.CharField('ISBN', max_length=13,
                   help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-details', args=[str(self.pk)])

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all() ]) #Great syntax

    class Meta:
        ordering = ["title"]



class Language(models.Model):
    language_name = models.CharField(max_length=50, help_text="Language Name(e.g. Enlish, Hindi, Marathi etc.)")

    def __str__(self):
        return self.language_name

class Author(models.Model):
    name = models.CharField(max_length=200)
    dob = models.DateField(null=True, blank=True)
    dod = models.DateField('Died', blank=True, null=True,help_text = "Date of death of the author",)
    #books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author-details', args=[str(self.id)])

    class Meta:
        ordering=["name"]

class BookInstance(models.Model):
    books_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               help_text="Help text for this particular book instance")
    book = models.ForeignKey(Book, on_delete = models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(help_text="Expected return date of the book", null=True, blank=True)
    language = models.ForeignKey(Language, on_delete = models.SET_NULL, null="True", blank="True")
    LOAN_STATUS = (('M','Maintenance'),('A','Available'),('R','Reserved'),('O','On Loan'))

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='A', help_text='Book availability')
    borrower = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return '{0},({1})'.format(self.book_id,self.book.title)

    @property
    def is_overdue(self):
        if self.due_back and datetime.date.today()>self.due_back:
            return True
        return False



