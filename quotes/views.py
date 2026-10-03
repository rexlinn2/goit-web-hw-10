from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AuthorForm, QuoteForm
from .models import Author, Quote

def home(request):
    tag = request.GET.get('tag')
    qs = Quote.objects.select_related('author').all().order_by('id')
    if tag: qs = [q for q in qs if tag in q.tags]
    page = Paginator(qs, 10).get_page(request.GET.get('page'))
    tags = {}
    for q in Quote.objects.all():
        for t in q.tags: tags[t] = tags.get(t, 0) + 1
    top_tags = sorted(tags.items(), key=lambda x: (-x[1], x[0]))[:10]
    return render(request, 'quotes/home.html', {'page':page,'top_tags':top_tags,'active_tag':tag})
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'quotes/author.html', {'author':author})
def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(); login(request, user); return redirect('home')
    return render(request, 'quotes/form.html', {'form':form,'title':'Реєстрація'})
@login_required
def add_author(request):
    form = AuthorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid(): form.save(); messages.success(request,'Автора додано.'); return redirect('home')
    return render(request,'quotes/form.html',{'form':form,'title':'Додати автора'})
@login_required
def add_quote(request):
    form = QuoteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid(): form.save(); messages.success(request,'Цитату додано.'); return redirect('home')
    return render(request,'quotes/form.html',{'form':form,'title':'Додати цитату'})
@login_required
def scrape_import(request):
    if request.method == 'POST':
        try:
            import requests
            from bs4 import BeautifulSoup
            url='https://quotes.toscrape.com/'
            added=0
            while url:
                soup=BeautifulSoup(requests.get(url, timeout=20).text,'html.parser')
                for item in soup.select('.quote'):
                    name=item.select_one('.author').get_text(strip=True)
                    author,_=Author.objects.get_or_create(fullname=name)
                    q=item.select_one('.text').get_text(strip=True)
                    tags=[x.get_text(strip=True).lower() for x in item.select('.tag')]
                    if not Quote.objects.filter(quote=q,author=author).exists(): Quote.objects.create(quote=q,author=author,tags=tags); added+=1
                nxt=soup.select_one('li.next a'); url=requests.compat.urljoin(url,nxt['href']) if nxt else None
            messages.success(request,f'Імпорт завершено. Додано цитат: {added}.')
        except Exception as e: messages.error(request,f'Помилка скрапінгу: {e}')
    return redirect('home')
