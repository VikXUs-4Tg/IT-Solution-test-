from django.shortcuts import render, redirect
from .models import Quote, Source

import random

def random_quote_view(request):
    #Создание "стартовой" цитаты и источника в случае, когда база еще пуста (что бы открытие сайта не начиналось с ошибки)
    try:
        quote = Quote.objects.latest('id')
    except Quote.DoesNotExist:
        quote = Quote(text='Если бы гусеница держалась за прошлое, она бы никогда не стала бабочкой', source=Source.objects.create(name='Чесалов Ю.А.'))
        quote.save()
    #Алгоритм выбора случайной цитаты
    quotes = Quote.objects.all()
    random_quote = random.choices(quotes, weights=[quote.weight for quote in quotes])[0]
    #Реализация счётчика показов
    if request.method == 'GET':
        random_quote.impressions += 1
        random_quote.save()
    # Алгоритм обработки выставления оценки пользователем
    if request.method == 'POST':
        quote_id = request.POST.get('like') or request.POST.get('dislike')
        if quote_id:
            main_quote = Quote.objects.get(id=quote_id)
            if 'like' in request.POST:
                main_quote.likes += 1
            elif 'dislike' in request.POST:
                main_quote.dislikes += 1
            main_quote.save()
        return redirect('index')
    return render(request, 'shopapp/index.html', {'quote': random_quote})

def add_new_quote(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        source_name = request.POST.get('source')
        weight = int(request.POST.get('weight'))
        # Проверяем, существует ли цитата с таким текстом
        if Quote.objects.filter(text=text).exists():
            return render(request, 'shopapp/add_new_quote.html', {'text_error': 'Цитата уже существует.'})
        source, _ = Source.objects.get_or_create(name=source_name)
        # Проверяем количество цитат от этого источника
        if Quote.objects.filter(source=source).count() >= 3:
            return render(request, 'shopapp/add_new_quote.html', {'source_error': 'У этого источника уже есть три цитаты.'})
        quote = Quote(text=text, source=source, weight=weight)
        quote.save()
        return redirect('index')
    return render(request, 'shopapp/add_new_quote.html')

def popular_quotes(request):
    quotes = Quote.objects.all()
    quotes = sorted(quotes, key=lambda q: q.popularity, reverse=True)
    quotes = [q for q in quotes if q.popularity > 0][:10]
    return render(request, 'shopapp/popular_quotes.html', {'quotes': quotes})
