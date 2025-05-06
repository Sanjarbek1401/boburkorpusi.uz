from django import template
import re

register = template.Library()

@register.filter(name='highlight')
def highlight(text, query):
    """
    Template filter to highlight search terms in text
    """
    if not text or not query:
        return text
    
    # Split query into terms
    terms = query.split()
    
    # Highlight each term
    highlighted_text = text
    for term in terms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        highlighted_text = pattern.sub(lambda m: f'<mark>{m.group(0)}</mark>', highlighted_text)
    
    return highlighted_text

@register.filter(name='split_kwic')
def split_kwic(text, term):
    """
    Split text into before and after parts around the search term.
    Returns a dict with keys '0' (before) and '1' (after).
    """
    if not text or not term:
        return {'0': text, '1': ''}
    
    # Case insensitive search
    term_pattern = re.compile(re.escape(term), re.IGNORECASE)
    
    # Find the position of the term
    match = term_pattern.search(text)
    if match:
        before = text[:match.start()]
        after = text[match.end():]
        return {'0': before, '1': after}
    
    # If term not found, return entire text as "before"
    return {'0': text, '1': ''}