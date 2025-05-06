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
       def get_kwic_context(text, search_term, context_words=5):
           """
           Extract Key Word In Context for the search term.
           Returns a list of strings, each containing the search term in context.
           """
           # Split text into words
           words = text.split()
           # Find all occurrences of the search term
           matches = []
           for i, word in enumerate(words):
               if search_term.lower() in word.lower():
                   # Get context words before and after
                   start = max(0, i - context_words)
                   end = min(len(words), i + context_words + 1)
                   
                   # Create the before part
                   before_text = ' '.join(words[start:i])
                   if start > 0:
                       before_text = '... ' + before_text
                   
                   # Get the exact match word
                   matched_word = words[i]
                   
                   # Create the after part
                   after_text = ' '.join(words[i+1:end])
                   if end < len(words):
                       after_text = after_text + ' ...'
                   
                   # Combine to create the KWIC context
                   kwic_context = f"{before_text} {matched_word} {after_text}"
                   matches.append(kwic_context)
           return matches

       # Search in DevonText
       text_results = DevonText.objects.filter(text__icontains=query)
       for text in text_results:
           kwic_matches = get_kwic_context(text.text, query)
           if kwic_matches:
               results.append({
                   'type': 'Devon',
                   'title': f"{text.group.category.name} - {text.group.name}",
                   'sentences': kwic_matches,
                   'url': reverse('divan_text_detail', args=[text.group.id]),
                   'source': text.group.name
               })

       # Search in Baburnoma
       baburnoma_results = Baburnoma.objects.filter(
           Q(title__icontains=query) |
           Q(text_content__icontains=query)
       )
       for item in baburnoma_results:
           if item.text_content:
               kwic_matches = get_kwic_context(item.text_content, query)
               if kwic_matches:
                   results.append({
                       'type': 'Baburnoma',
                       'title': item.title,
                       'sentences': kwic_matches,
                       'url': reverse('baburnoma'),
                       'source': 'Baburnoma'
                   })

       # Search in Dictionary
       dictionary_results = Dictionary.objects.filter(
           Q(word__icontains=query) |
           Q(description__icontains=query)
       )
       for dict_item in dictionary_results:
           kwic_matches = get_kwic_context(dict_item.description, query)
           if kwic_matches:
               results.append({
                   'type': 'Lug\'at',
                   'title': dict_item.word,
                   'sentences': kwic_matches,
                   'url': reverse('dictionary_list') + f'?q={query}',
                   'source': 'Lug\'at'
               })

   # Implement pagination
   paginator = Paginator(results, 30)  # Show 30 results per page
   page_number = request.GET.get('page', 1)
   try:
       page_obj = paginator.page(page_number)
   except:
       page_obj = paginator.page(1)  # Default to first page on error

   context = {
       'query': query,
       'results': page_obj,
       'count': len(results),
       'total_pages': paginator.num_pages,
       'current_page': int(page_number)
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




