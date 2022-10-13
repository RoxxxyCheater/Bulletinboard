from importlib.resources import contents
from unicodedata import category
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView,CreateView,UpdateView, DeleteView
from django.http import HttpResponse
from .models import Ad,Comment as Comments,FeedFile, User,Category
from .forms import *
#from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import AdForm
import os, re
#from sign.views import upgrade_me
from django.contrib.auth.decorators import login_required


class Ads(ListView):
    model = Ad
    template_name = 'ads_all.html'
    context_object_name = 'ads_all'
    queryset = Ad.objects.order_by('-id')

    def get_context_data(self, **kwargs): #переопределяем метод получения контекста
        context = super().get_context_data(**kwargs) #получили весь контекст из класса-родителя
        context['is_authors'] = self.request.user.groups.filter(name = 'authors').exists()
        context['user_info'] = self.request.user
        return context #возвращаем контекст обратно





class AdDetail(DetailView):
    model = Ad
    template_name = 'ad.html'
    context_object_name = 'Ad'
    permission_required = 'bulletinboardapp.add_ad'
    queryset = Ad.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.object.id)
        print('////!!!!', Comments.objects.all().values())
        ad_filess = FeedFile.objects.filter(file_id = self.object.id).values()
        context['ad_files'] = FeedFile.objects.filter(file_id = self.object.id).values()
        context['file_list'] = FeedFile.objects.filter()
        filename, file_extension = os.path.splitext(str(ad_filess))
        context['file_extension'] = file_extension[0:-4]
        context['comments'] = Comments.objects.filter(Ad = self.object)
        print(self.request.GET.get('pk'))
        return context


    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            ad_id = self.kwargs.get('pk')
            new_comment = Comments.objects.create(
                Ad = Ad.objects.get(id = ad_id),
                commAuthor= request.user,
                content =  request.POST.get('subject'),
                accepted = False,
            )
            #print('@@@@',newMailSub, '@@@@', newMailSub.client_title, '@@@@', newMailSub.message, '@@@@', newMailSub.category, '@@@@', newMailSub.subscriber, '@@@@', newMailSub.subscriber_email)
            new_comment.save()
        return redirect('/callboard/'+ str(ad_id))
        

class Author(ListView):
    model = User
    template_name = 'authors.html'
    context_object_name = 'authors'

class Comment(ListView):
    model = Comments
    template_name = 'comments.html'
    context_object_name = 'comment_all'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['comments'] = Comments.objects.filter(commAuthor_id = self.request.user.id)
        posts_user = Ad.objects.filter(author=self.request.user)
        context['comments_all']= []
        context['posts_all']= []

        for post in posts_user:
            context['posts_all'].append(post)
            com = Comments.objects.filter(Ad = post).values().first()
            context['comments_all'].append(com)
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            decline = request.POST.get('decline')
            accept = request.POST.get('accept')
            if decline:
                comment = Comments.objects.get(id = decline)
                comment.accepted = False
            elif accept:
                comment = Comments.objects.get(id = accept)
                comment.accepted = True
            comment.save()
        return redirect('/callboard/comments/')
        
class AdAdd(LoginRequiredMixin,CreateView):
    template_name = 'add_ad.html'  # Replace with your template.
    success_url = '/callboard/'  # Replace with your URL or reverse().
    permission_required = 'bulletinboardapp.add_ad'
    form_class = AdForm
    print(form_class)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result_file = FeedFile.objects.all()
        context['result_file'] = result_file.values()
        #context['actual_user'] = ((User.objects.filter(id=self.request.user.id).values()).first())['username']
        return context
    
    def post(self, request, *args, **kwargs):
        post_save_request = super().post(request, *args, **kwargs)
        if request.method == 'POST':
            post = Ad.objects.create(
                author=request.user, 
                category=Category.objects.get(id = self.request.POST['category']),
                title=request.POST['title'],
                content=request.POST['content']
            )
            files = request.FILES.getlist('files') # name from forms

            for file in files:
                filetype = re.split('/',str(file.content_type))[0]
                print(file.content_type, filetype)
                files_upload = FeedFile.objects.create(file = post, filefield = file, filetype = re.split('/',str(file.content_type))[0])
                files_upload.save()
            print('!!Files:', files)
        post.save()
           
        return post_save_request



class AdUpdateView(UpdateView):
    template_name = 'ad_update.html'
    form_class = AdForm
    model = Ad
    success_url = '/callboard/'
    permission_required = 'bulletinboardapp.ad_update'
        
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Ad.objects.get(pk=id)

class AdDeleteView(DeleteView):
    template_name = 'ad_delete.html'
    model = Ad
    queryset = Ad.objects.all()
    success_url = '/callboard/'
    permission_required = 'bulletinboardapp.ad_delete'
