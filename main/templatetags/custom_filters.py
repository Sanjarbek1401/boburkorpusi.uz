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