from django.shortcuts import render, redirect
from .models import Quote
import random

def random_quote_view(request):
    quotes = Quote.objects.all()
    #random_quote = random.choice(quotes)
    random_quote = random.choices(quotes, weights=[quote.weight for quote in quotes])[0]
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