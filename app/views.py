from django.shortcuts import render
from django.views import View
from app.models import Book, Author
from django.db.models import Avg, Count, Min, OuterRef, Subquery


# Create your views here.


class BookView(View):

    def get(self, request):
        filter = request.GET.get('filter')
        authors = Author.objects.all()
        if filter:
            if filter == 'every_writer_s_count_of_books':
                authors = Author.objects.annotate(book_data=Count('books')).order_by('-book_data')
                context = {
                    'authors': authors
                }

            elif filter == 'every_writer_s_most_valuable_book':
                max_price_book_subquery = Book.objects.filter(author=OuterRef('pk')).order_by('-price').values('price')[
                                        :1]
                authors = Author.objects.annotate(book_data=Subquery(max_price_book_subquery)).order_by('-book_data')
                context = {
                    'authors': authors
                }

            elif filter == 'every_writer_s_cheapest_book':
                authors = Author.objects.annotate(book_data=Min('books__price')).order_by('-book_data')
                context = {
                    'authors': authors
                }

            elif filter == 'the_average_of_each_writer_s_cheapest_book':
                authors = Author.objects.annotate(book_data=Avg('books__price')).order_by('-book_data')
                context = {
                    'authors': authors
                }

        context = {
            'authors': authors
        }
        return render(request, 'app/index.html', context)
