import article
from django.shortcuts import get_list_or_404, render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import ArticleForm
from django.contrib import messages
from .models import Article, Comment

from django.contrib.auth.decorators import login_required
# Create your views here.

def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request, "articles.html", {"articles":articles})
    else:
        articles = Article.objects.all()
        return render(request, "articles.html", {"articles": articles} )

def index(request):
    #return HttpResponse("<h3> Main Page</h3>")
    return render(request, "index.html", {"number": 7})


def about(request):
    return render(request, "about.html")

@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles": articles
    }
    return render(request, "dashboard.html", context)  

@login_required(login_url="user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        article = form.save(commit= False )
        article.author = request.user
        article.save()
        messages.success(request, "You successfully created an article!")

        articles = Article.objects.filter(author = request.user)
        context = {
            "articles": articles
        }
        return render(request,"dashboard.html", context) 

    return render(request, "addarticle.html", {"form":form}) 

def detail(request, id):
    #article =  Article.objects.filter(id = id).first()
    article =  get_object_or_404(Article, id = id)
    comments = article.comments.all()
    return render(request, "detail.html", {"article": article, "comments":comments})

@login_required(login_url="user:login")
def editArticle(request, id):
    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        article = form.save(commit= False )
        article.author = request.user
        article.save()
        messages.success(request, "You successfully updated the article!")

        articles = Article.objects.filter(author = request.user)
        return render(request, "dashboard.html", {"articles": articles})

    return render(request, "edit.html", {"form":form})

@login_required(login_url="user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id=id)
    deleted_title = article.title
    article.delete()
    messages.success(request, "You successfully deleted the article titled:  \"  " + str(deleted_title) + " \"")
    return redirect("article:dashboard")


def addComment(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        new_comment = Comment(comment_author = comment_author, comment_content= comment_content)
        new_comment.article = article
        new_comment.save()
    #return redirect("/articles/asdf/" + str(id))
    return redirect(reverse("article:detail", kwargs={"id":id}))

