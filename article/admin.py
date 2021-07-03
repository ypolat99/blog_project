from django.contrib import admin
from .models import Article, Comment
# Register your models here.

admin.site.register(Comment)


#used the following link --> https://docs.djangoproject.com/en/3.2/ref/contrib/admin/
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_date"]
    list_display_links = ["title", "created_date"]
    list_filter = ["created_date"]
    search_fields = ["title"]
    class Meta:
      model = Article
    
    