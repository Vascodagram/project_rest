from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class Category(models.Model):
    name = models.CharField('Категорія', max_length=100)
    slug = models.SlugField('slag')

    def __str__(self):
        return self.name


class Post(models.Model):
    categories = models.ForeignKey('Category', verbose_name='Категорія', on_delete=models.SET_NULL, null=True)
    title = models.CharField('Назва', max_length=250)
    anons = models.CharField("Анонс", max_length=250)
    full_text = RichTextUploadingField("Стаття")
    date = models.DateTimeField('дата опублікування')

    def __str__(self):
        return f"Назва ресторану: {self.title}, Категорія: {self.categories}"
    
    def get_review(self):
        return self.comment_post.filter(parent__isnull=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comment_post', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор коментаря", blank=True, null=True)
    create_data = models.DateTimeField(auto_now=True)
    body = models.TextField(verbose_name='Текст коментаря', max_length=150)
    status = models.BooleanField(verbose_name="Статус коментаря", default=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def get_children(self):
        print(self)
        return Comment.objects.filter(parent=self)

    class Meta:
        ordering = ['-create_data']

    def __str__(self):
        return f'Comment by {self.user}, post: {self.post}'

