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
       baburnoma = Baburnoma.objects.latest('uploaded_at')
       return FileResponse(baburnoma.pdf_file, content_type='application/pdf')
   except Baburnoma.DoesNotExist:
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

       # Search in Baburnoma (title and text_content)
       baburnoma_results = Baburnoma.objects.filter(
           Q(title__icontains=query) |
           Q(text_content__icontains=query)
       )
       for item in baburnoma_results:
           matching_sentences = []
           if query.lower() in item.title.lower():
               matching_sentences.append(item.title)
           
           # Search in text_content if available
           if item.text_content:
               text_matches = extract_sentences(item.text_content, query)
               matching_sentences.extend(text_matches)

           if matching_sentences:
               # Highlight the matches
               highlighted_title = highlight_text(item.title, query)
               highlighted_sentences = [highlight_text(sentence, query) for sentence in matching_sentences[1:]] if len(matching_sentences) > 1 else []
               results.append({
                   'type': 'Baburnoma',
                   'title': highlighted_title,
                   'sentences': highlighted_sentences,
                   'url': reverse('baburnoma', args=[]),
                   'source': 'Baburnoma'
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
   # Convert text and query to lowercase for case-insensitive matching
   text_lower = text.lower()
   # Split query into individual terms and clean them
   terms = [term.strip() for term in query.lower().split()]

   # Find all occurrences of each term
   positions = []
   for term in terms:
       start = 0
       while True:
           start = text_lower.find(term, start)
           if start == -1:  # term not found
               break
           positions.append((start, start + len(term)))
           start += 1

   # Sort positions and merge overlapping ranges
   if not positions:
       return text

   positions.sort()
   merged = [positions[0]]
   for current in positions[1:]:
       if current[0] <= merged[-1][1]:
           # Ranges overlap, merge them
           merged[-1] = (merged[-1][0], max(merged[-1][1], current[1]))
       else:
           merged.append(current)

   # Build the highlighted text
   result = []
   last_end = 0
   for start, end in merged:
       result.append(text[last_end:start])
       result.append(f'<mark>{text[start:end]}</mark>')
       last_end = end
   result.append(text[last_end:])

   return ''.join(result)

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
    
    if word_query:
        # Exact word search
        queryset = Dictionary.objects.filter(word__iexact=word_query)
    elif query:
        # General search in both word and description
        queryset = Dictionary.objects.filter(
            Q(word__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        # No search query - get all words
        queryset = Dictionary.objects.all()
    
    # Sort in Uzbek alphabet order
    words = Dictionary.get_ordered_queryset()
    
    # Get unique first letters for navigation
    first_letters = sorted(set(word.word[0].upper() for word in words))
    
    context = {
        'words': words,
        'first_letters': first_letters,
        'query': query,
        'word_query': word_query
    }
    return render(request, 'dictionary_list.html', context)

def uzbek_order(word):
    # O'zbek alifbosi tartibida so'zlarni saralash uchun yordamchi funksiya
    uzbek_alphabet = 'a b d e f g h i j k l m n o p q r s t u v x y z oʻ gʻ sh ch ng'
    order_dict = {char: i for i, char in enumerate(uzbek_alphabet)}
    return [order_dict.get(c, len(uzbek_alphabet)) for c in word.lower()]