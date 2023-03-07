from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text': 'Текс поста',
            'group': 'Группа',
        }
        help_text = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост',
        }

    def clean(self):
        text = self.cleaned_data.get('text')
        if not text:
            raise forms.ValidationError("Поле должно быть заполнено")
        return self.cleaned_data
