from django import forms
from .models import Review


from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

# In forms.py
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('media_type', 'media_title', 'review_title', 'review_text', 'rating', 'episode_number', 'media_image')
        widgets = {
            'media_type': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Selecione o tipo de mídia'
            }),
            'media_title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome da obra'
            }),
            'review_title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Título da sua crítica'
            }),
            'review_text': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Escreva sua crítica aqui'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control', 
                'type': 'range', 
                'min': 0.5, 
                'max': 5,
                'step': 0.5
            }),
            'episode_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Número do episódio (opcional)'
            }),
            'media_image': forms.FileInput(attrs={
                'class': 'form-control-file', 
                'accept': 'image/jpeg,image/png,image/gif,image/webp'
            }),
        }