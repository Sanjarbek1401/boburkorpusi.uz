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
   baburnoma_results = []  # Separate list for Baburnoma results

   if query:
       def get_kwic_context(text, search_term, context_words=5):
           """
           Extract Key Word In Context for the search term.
           Returns a list of strings, each containing the search term in context.
           """
           if not text or not search_term:
               return []
               
           # Find exact word matches with the new function
           word_matches = find_word_with_suffixes(text, search_term)
           
           # If no matches found with exact word matching, return empty list
           if not word_matches:
               return []
           
           matches = []
           # Split text into words to get context
           words = text.split()
           
           for matched_word, start_pos, end_pos in word_matches:
               # Create a substring containing words around the match
               # Calculate approximate character positions for context
               # Get about 5 words before and after
               context_chars = 40  # Approximate character count for context words
               
               context_start = max(0, start_pos - context_chars)
               context_end = min(len(text), end_pos + context_chars)
               
               # Extract the context substring
               before_text = text[context_start:start_pos].strip()
               after_text = text[end_pos:context_end].strip()
               
               # Add ellipsis if we truncated the context
               if context_start > 0:
                   before_text = "... " + before_text
               if context_end < len(text):
                   after_text = after_text + " ..."
               
               # Combine the context
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
       baburnoma_items = Baburnoma.objects.filter(
           Q(title__icontains=query) |
           Q(text_content__icontains=query)
       )
       for item in baburnoma_items:
           if item.text_content:
               kwic_matches = get_kwic_context(item.text_content, query)
               if kwic_matches:
                   baburnoma_results.append({
                       'type': 'Baburnoma',
                       'title': item.title,
                       'sentences': kwic_matches,
                       'url': reverse('baburnoma'),
                       'source': 'Baburnoma',
                       'chapter': item.chapter if hasattr(item, 'chapter') else None
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

   # Store the original counts before pagination
   total_result_count = len(results)  # Other results (Devon + Dictionary)
   total_baburnoma_count = len(baburnoma_results)  # Baburnoma results
   total_results_count = total_result_count + total_baburnoma_count  # Combined total

   # Implement pagination for main results
   paginator = Paginator(results, 30)  # Show 30 results per page
   page_number = request.GET.get('page', 1)
   try:
       page_obj = paginator.page(page_number)
   except:
       page_obj = paginator.page(1)  # Default to first page on error
       
   # Implement pagination for Baburnoma results
   baburnoma_paginator = Paginator(baburnoma_results, 10)  # Show 10 Baburnoma results per page
   baburnoma_page = request.GET.get('baburnoma_page', 1)
   try:
       baburnoma_page_obj = baburnoma_paginator.page(baburnoma_page)
   except:
       baburnoma_page_obj = baburnoma_paginator.page(1)

   # Calculate displayed count
   total_displayed = len(page_obj) + len(baburnoma_page_obj)

   context = {
       'query': query,
       'results': page_obj,
       'count': total_result_count,  # Use original count before pagination
       'total_pages': paginator.num_pages,
       'current_page': int(page_number),
       'baburnoma_results': baburnoma_page_obj,
       'baburnoma_count': total_baburnoma_count,  # Use original count before pagination
       'baburnoma_total_pages': baburnoma_paginator.num_pages,
       'baburnoma_current_page': int(baburnoma_page),
       'total_results_count': total_results_count,
       'total_displayed': total_displayed
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
   if not query or not text:
       return text
       
   # Split query into individual terms and clean them
   terms = [term.strip() for term in query.lower().split() if term.strip()]
   if not terms:
       return text
       
   # Find all occurrences of each term with suffix matching
   positions = []
   for term in terms:
       # Find matches including words with suffixes
       matches = find_word_with_suffixes(text, term)
       for _, start, end in matches:
           positions.append((start, end))

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
        queryset = Dictionary.objects.filter(word__iexact=word_query)
    elif query:
        queryset = Dictionary.objects.filter(
            Q(word__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        queryset = Dictionary.objects.all()
    
    # Sort the filtered queryset in Uzbek alphabet order
    words = sorted(queryset, key=lambda x: uzbek_order(x.word))
    
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

def find_word_with_suffixes(text, search_word):
    """
    Finds exact word matches and their suffix forms in a given text.
    
    Args:
        text (str): The text to search in.
        search_word (str): The base word to search for.
        
    Returns:
        list: A list of tuples containing (matched_word, start_position, end_position)
    """
    if not search_word or not text:
        return []
    
    # Add spaces and common punctuation before text to help with boundary detection
    text = " " + text
    
    # Define acceptable word boundary characters (space, punctuation, start/end of string)
    boundary_chars = r'[\s,.!?;:"\'()\[\]{}]'
    
    # Create a pattern that matches:
    # 1. A word boundary character before our word
    # 2. The exact search word
    # 3. Optional Uzbek suffixes after the word
    # 4. A word boundary at the end
    pattern = f'({boundary_chars})({re.escape(search_word)})(\w*?)(?={boundary_chars}|$)'
    
    matches = []
    for match in re.finditer(pattern, text, re.IGNORECASE):
        # Get the full match without the leading boundary character
        # Combine base word with its suffix
        matched_word = match.group(2) + match.group(3)
        
        # Adjust the start position to account for the added space at the beginning
        start_pos = match.start(2) - 1  # -1 to account for the space we added
        end_pos = match.end(3) - 1      # -1 to account for the space we added
        
        # Only include if this is truly a word match (not part of another word)
        matches.append((matched_word, start_pos, end_pos))
    
    return matches




