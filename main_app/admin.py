from django.contrib import admin
from django import forms
from .models import Post, Category, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# Register your models here.


class PostAdminForm(forms.ModelForm):
    full_text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
