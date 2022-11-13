from enum import auto
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache


# class Author(models.Model):
#     authors = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.authors.username}'

class Category(models.Model):
    catName = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return f'{self.catName}'


class Ad(models.Model):
#   TANKS = 'TK' HILLS = 'HL' SELLERS = 'SL' GUILDMASTERS = 'GM' QUESTGIVERS = 'QG' BLACKSMITHS = 'BS' CURRIERS = 'CR' POTIONS = 'PS' SPELLMASTERS = 'SP'
    author = models.ForeignKey(User, on_delete=models.CASCADE) #models.ForeignKey(Author, on_delete=models.CASCADE)
    created_ad = models.DateTimeField(auto_now_add=True)
    category =  models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(default='content')

    def __str__(self):
        return '%s %s %s %s %s' % (self.created_ad, self.author.username, self.title, self.content, self.preview())

    def preview(self):
        return self.content[:124] + '...'

    # def get_absolute_url(self):  # aбсолютный путь для перенаправления запроса
    #     return f'/bulletinboardapp/{self.id}' 
class FeedFile(models.Model):
    file=models.ForeignKey(Ad, on_delete=models.CASCADE)
    filefield = models.FileField(upload_to="static/files/%Y/%m/%d")
    filetype = models.TextField(default=None)

# class AdFileBr(models.Model):
#     ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
#     file = models.ForeignKey(FeedFile, on_delete=models.CASCADE)


class Comment(models.Model):
    Ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    commAuthor = models.ForeignKey(User,default='Guest ', on_delete=models.CASCADE)
    content = models.TextField()
    accepted = models.BooleanField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s %s %s %s %s %s' % (self.commAuthor.username, self.commAuthor.id, self.created_at, self.content, self.accepted, self.preview(), self.Ad)
            
    def preview(self):
        return self.content[:124] + '...'






# # Create your models here.
# # Здравствуйте, Олег!
# # Hi!


#  Нам необходимо разработать интернет-ресурс для фанатского сервера одной известной
# MMORPG — что-то вроде доски объявлений.# #Пользователи нашего ресурса должны иметь
# возможность зарегистрироваться в нём по e-mail, получив письмо с кодом подтверждения
# регистрации. После регистрации им становится доступно создание и редактирование объявлений.
# Объявления состоят из заголовка и текста, внутри которого могут быть картинки, встроенные
# видео и другой контент. Пользователи могут отправлять отклики на объявления других
# пользователей, состоящие из простого текста. При отправке отклика пользователь должен
# получить e-mail с оповещением о нём. Также пользователю должна быть доступна приватная
# страница с откликами на его объявления, внутри которой он может фильтровать отклики
# по объявлениям, удалять их и принимать (при принятии отклика пользователю, оставившему
# отклик, также должно прийти уведомление). Кроме того, пользователь обязательно должен
#  определить объявление в одну из следующих категорий: Танки, Хилы, ДД, Торговцы,
# #Гилдмастеры, Квестгиверы, Кузнецы, Кожевники, Зельевары, Мастера заклинаний.

# # Также мы бы хотели иметь возможность отправлять пользователям новостные рассылки.

# # Заранее спасибо! 





