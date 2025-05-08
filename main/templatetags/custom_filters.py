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
    This filter handles both exact matches and word-with-suffix matches.
    """
    if not text or not term:
        return {'0': text, '1': ''}
    
    # Define boundary chars for word boundary detection
    boundary_chars = r'[\s,.!?;:"\'()\[\]{}]'
    
    # Create a pattern that can find the term at word boundaries
    # This pattern will find the term as a whole word or at the start of a word (for suffix matches)
    term_pattern = rf'({boundary_chars}|^)({re.escape(term)}\w*?)({boundary_chars}|$)'
    
    # Find the position of the term
    match = re.search(term_pattern, " " + text, re.IGNORECASE)
    if match:
        # Find the actual matched word (including any suffix)
        matched_word = match.group(2)
        
        # Calculate the start/end positions in the original text
        # -1 to account for the space we added at the beginning
        start_pos = match.start(2) - 1
        end_pos = match.end(2) - 1
        
        # Extract the before and after parts
        before = text[:start_pos]
        after = text[end_pos:]
        
        # For display purposes, we want to show the exact match in the middle column
        # So we use the original term as part of the "before" text, and any suffix as part of "after"
        if len(matched_word) > len(term):
            # If matched word is longer than the search term (has a suffix)
            term_end = start_pos + len(term)
            suffix = text[term_end:end_pos]
            
            # Move suffix to the "after" part
            after = suffix + after
            
        return {'0': before, '1': after}
    
    # Use fallback method if term not found with word boundary approach
    # Simple substring search
    term_fallback = re.compile(re.escape(term), re.IGNORECASE)
    match = term_fallback.search(text)
    if match:
        before = text[:match.start()]
        after = text[match.end():]
        return {'0': before, '1': after}
    
    # If term not found at all, return entire text as "before"
    return {'0': text, '1': ''}

@register.filter(name='find_exact_match')
def find_exact_match(text, term):
    """
    Finds the exact word match in the text, including any suffixes.
    Returns the matched word or the original term if no match found.
    """
    if not text or not term:
        return term
    
    # Define boundary chars for word boundary detection
    boundary_chars = r'[\s,.!?;:"\'()\[\]{}]'
    
    # Create a pattern that matches the term with any suffix, with word boundaries
    pattern = rf'({boundary_chars}|^)({re.escape(term)}\w*?)({boundary_chars}|$)'
    
    # Search for the pattern in the text
    match = re.search(pattern, " " + text, re.IGNORECASE)
    if match:
        # Return the matched word (group 2 contains the actual word match)
        return match.group(2)
    
    # If not found, return the original term
    return term