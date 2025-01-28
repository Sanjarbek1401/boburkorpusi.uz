from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.urls import reverse
from django.db.models import Q
import re
from .models import *
from django.core.paginator import Paginator

def home(request):
   return render(request, 'home.html')

def author(request):
   # Temporarily remove database query until model is ready
   return render(request, 'author.html', {'author': None})

def baburnoma(request):
   try:
       # Get the latest uploaded Boburnoma PDF
       boburnoma = Boburnoma.objects.latest('uploaded_at')
       return FileResponse(boburnoma.pdf_file, content_type='application/pdf')
   except Boburnoma.DoesNotExist:
       return render(request, 'baburnoma.html', {'error': "Hozircha PDF fayl mavjud emas"})

def search(request):
   query = request.GET.get('q', '')
   results = []

   if query:
       def extract_sentences(text, search_terms):
           # Split text into sentences (considering basic punctuation)
           sentences = [s.strip() for s in re.split('[.!?]', text) if s.strip()]
           matching_sentences = []

           # Convert search terms to list and clean them
           terms = [term.strip().lower() for term in search_terms.split()]

           for sentence in sentences:
               # Check if any search term is in the sentence
               if any(term in sentence.lower() for term in terms):
                   matching_sentences.append(sentence)

           return matching_sentences

       # Lug'atdan qidirish
       dictionary_results = Dictionary.objects.filter(
           Q(word__icontains=query) |
           Q(description__icontains=query)
       )
       for dict_item in dictionary_results:
           results.append({
               'type': 'Lug\'at',
               'title': highlight_text(dict_item.word, query),
               'sentences': [highlight_text(dict_item.description, query)],
               'url': reverse('dictionary_list') + f'?q={query}',
               'source': 'Lug\'at'
           })

       # Search in DevonText
       text_results = DevonText.objects.filter(text__icontains=query)
       for text in text_results:
           matching_sentences = extract_sentences(text.text, query)
           if matching_sentences:
               # Highlight matched sentences
               highlighted_sentences = [highlight_text(sentence, query) for sentence in matching_sentences]
               results.append({
                   'type': 'Devon',
                   'title': f"{text.group.category.name} - {text.group.name}",
                   'sentences': highlighted_sentences,
                   'url': reverse('divan_text_detail', args=[text.group.id]),
                   'source': text.group.name
               })

       # Search in Baburnoma (only title field)
       baburnoma_results = Baburnoma.objects.filter(title__icontains=query)
       for item in baburnoma_results:
           matching_sentences = []
           if query.lower() in item.title.lower():
               matching_sentences.append(item.title)

           if matching_sentences:
               # Highlight the title
               highlighted_title = highlight_text(item.title, query)
               results.append({
                   'type': 'Boburnoma',
                   'title': highlighted_title,
                   'sentences': [],
                   'url': reverse('baburnoma_detail', args=[item.id]),
                   'source': 'Boburnoma'
               })

   context = {
       'query': query,
       'results': results,
       'count': len(results)
   }
   return render(request, 'search_results.html', context)

def highlight_text(text, query):
   """
   Highlights occurrences of query terms in the given text.

   Args:
       text (str): The text to search and highlight terms in.
       query (str): The query string containing one or more search terms.

   Returns:
       str: The text with highlighted search terms wrapped in <mark> tags.
   """
   # Split the query into individual terms
   terms = query.split()
   highlighted_text = text

   # Apply highlighting for each term
   for term in terms:
       # Compile a case-insensitive regex pattern for the term
       pattern = re.compile(re.escape(term), re.IGNORECASE)
       highlighted_text = pattern.sub(lambda m: f'<mark>{m.group(0)}</mark>', highlighted_text)

   return highlighted_text

def contact(request):
   # Temporarily remove database query until model is ready
   return render(request, 'contact.html', {'contacts': []})

def divan(request):
   categories = DevonCategory.objects.all().order_by('order')
   return render(request, 'divan.html', {'categories': categories})

def divan_category(request, category_id):
   category = get_object_or_404(DevonCategory, id=category_id)
   groups = DevonGroup.objects.filter(category=category).order_by('order')
   return render(request, 'divan_category.html', {
       'category': category,
       'items': groups
   })

def divan_text_detail(request, group_id):
   group = get_object_or_404(DevonGroup, id=group_id)
   texts = DevonText.objects.filter(group=group).order_by('order')
   return render(request, 'divan_text_detail.html', {
       'group': group,
       'texts': texts
   })

def work_detail(request, work_id):
   work = get_object_or_404(Work, id=work_id)
   return render(request, 'work_detail.html', {
       'work': work
   })


def dictionary_list(request):
    query = request.GET.get('q', '')
    word_query = request.GET.get('word', '')

    words = Dictionary.objects.all()

    if word_query:
        # Faqat so'z bo'yicha qidirish
        words = words.filter(word__icontains=word_query)
    elif query:
        # So'z va izohlar bo'yicha qidirish
        words = words.filter(
            Q(word__icontains=query) |
            Q(description__icontains=query)
        )

    # O'zbek alifbosi bo'yicha saralash
    words = sorted(words, key=lambda x: uzbek_order(x.word))

    paginator = Paginator(words, 20)
    page = request.GET.get('page')
    words = paginator.get_page(page)

    return render(request, 'dictionary_list.html', {
        'words': words,
        'query': query,
        'word_query': word_query
    })

def uzbek_order(word):
    """O'zbek alifbosi tartibida so'zlarni saralash uchun yordamchi funksiya"""
    uzbek_alphabet = 'a b d e f g h i j k l m n o p q r s t u v x y z oʻ gʻ sh ch ng'
    order_dict = {char: i for i, char in enumerate(uzbek_alphabet)}
    return [order_dict.get(c, len(uzbek_alphabet)) for c in word.lower()]