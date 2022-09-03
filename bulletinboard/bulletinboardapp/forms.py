from django.forms import ModelForm, BooleanField
from .models import Ad
from django import forms
 
 
# Создаём модельную форму
class AdForm(ModelForm):
    check_box = BooleanField(label='Я ознакомлен в полном обьёме с правилами ресурса, относительно публикаций и обработки персональных данных авторов статей. Данным действием Соглашаюсь с правилами ресурса.')  #добавляем галочку или же true-false поле , 'check_box'
    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Ad
        fields = ['author','category','title', 'content', 'check_box']
        



class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))