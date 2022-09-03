from socket import AddressInfo
from django.shortcuts import render
from django.views.generic import ListView, DetailView,CreateView,UpdateView, DeleteView # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.http import HttpResponse
from bulletinboardapp.models import *
from .forms import *
from django.views.generic.edit import FormView
from .forms import FileFieldForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class Ads(ListView):
    model = Ad
    template_name = 'ads_all.html'
    context_object_name = 'ads_all'
    queryset = Ad.objects.order_by('-id')

    def get_context_data(self, **kwargs): #переопределяем метод получения контекста
        context = super().get_context_data(**kwargs) #получили весь контекст из класса-родителя
        context['is_authors'] = self.request.user.groups.filter(name = 'authors').exists()
        context['user_info'] = self.request.user
        #добавили новую контекстную переменную is_authors
        #есть ли пользователь в группе - заходим в переменную запроса self.request/
        #Из этой переменной мы можем вытащить текущего пользователя
        #В поле groups хранятся все группы, в которых он состоит
        #применяем фильтр к этим группам и ищем ту самую, имя которой premium.
        #проверяем, есть ли какие-то значения в отфильтрованном списке.
        #Mетод exists() вернёт True, если группа premium в списке групп пользователя найдена
        #нам нужно получить наоборот — True, если пользователь не находится в этой группе, поэтому добавляем отрицание not
        return context #возвращаем контекст обратно





class Ad(DetailView):
    model = Ad
    template_name = 'authors.html'
    context_object_name = 'Ad'

class Author(ListView):
    model = Author
    template_name = 'authors.html'
    context_object_name = 'authors'

class Comment(ListView):
    model = Comment
    template_name = 'comments.html'
    context_object_name = 'comment_all'

class AdAdd(CreateView):
    template_name = 'add_ad.html'
    form_class = AdForm

    success_url = '/callboard/'

    # def author_add(self, request):
    #     if request.method == 'POST':
    #         new_author = Author(authors =User.objects.get(username=request.POST.get('username')))

    #     print(self,request )
    #     return new_author
    #return redirect('/news/search')


# class ad(DetailView):
#     pass
# class ads(ListView):
#     pass
# class create_ad(CreateView):
#     pass
# class edit_ad(UpdateView):
#     pass
# class delete_ad(DeleteView):
#     pass
 
