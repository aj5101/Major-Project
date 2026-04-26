"""
Text Simplification Module

Simplifies text to make it age-appropriate for children (ages 6-12).
Uses rule-based and ML-based approaches to simplify vocabulary and sentence structure.
"""

import re
from typing import List

class TextSimplifier:
    """
    Text simplifier for children's content.
    
    Simplifies vocabulary, sentence structure, and removes complex concepts
    to make content accessible for hearing-impaired children.
    """
    
    def __init__(self):
        """Initialize simplifier with vocabulary mappings"""
        # Common word simplifications (can be expanded)
        self.simplifications = {
            "utilize": "use",
            "approximately": "about",
            "demonstrate": "show",
            "facilitate": "help",
            "implement": "do",
            "significant": "important",
            "numerous": "many",
            "various": "different",
            "acquire": "get",
            "comprehend": "understand",
            "examine": "look at",
            "indicate": "show",
            "obtain": "get",
            "participate": "join",
            "require": "need",
            "reside": "live",
            "terminate": "end",
            "utilize": "use",
            "verify": "check"
        }
    
    async def simplify(self, text: str, target_age: int = 8) -> str:
        """
        Simplify text for target age group.
        
        Args:
            text: Original text
            target_age: Target age (6-12)
            
        Returns:
            simplified_text: Simplified version
        """
        if not text:
            return ""
        
        # Step 1: Replace complex words
        simplified = self._replace_complex_words(text)
        
        # Step 2: Break long sentences
        simplified = self._break_long_sentences(simplified, target_age)
        
        # Step 3: Remove complex punctuation
        simplified = self._simplify_punctuation(simplified)
        
        # Step 4: Ensure clarity
        simplified = self._ensure_clarity(simplified)
        
        return simplified.strip()
    
    def _replace_complex_words(self, text: str) -> str:
        """
        Replace complex words with simpler alternatives.
        
        Args:
            text: Original text
            
        Returns:
            text with simplified vocabulary
        """
        words = text.split()
        simplified_words = []
        
        for word in words:
            # Remove punctuation for lookup
            clean_word = re.sub(r'[^\w]', '', word.lower())
            
            if clean_word in self.simplifications:
                # Preserve original capitalization/punctuation
                replacement = self.simplifications[clean_word]
                if word[0].isupper():
                    replacement = replacement.capitalize()
                # Add back punctuation
                if not word[-1].isalnum():
                    replacement += word[-1]
                simplified_words.append(replacement)
            else:
                simplified_words.append(word)
        
        return " ".join(simplified_words)
    
    def _break_long_sentences(self, text: str, target_age: int) -> str:
        """
        Break long sentences into shorter ones.
        
        Args:
            text: Text to process
            target_age: Target age (younger = shorter sentences)
            
        Returns:
            text with shorter sentences
        """
        # Maximum words per sentence based on age
        max_words = {
            6: 8,
            7: 10,
            8: 12,
            9: 14,
            10: 16,
            11: 18,
            12: 20
        }
        max_length = max_words.get(target_age, 12)
        
        sentences = re.split(r'([.!?]+)', text)
        result = []
        current_sentence = ""
        
        for i in range(0, len(sentences), 2):
            sentence = sentences[i] if i < len(sentences) else ""
            punctuation = sentences[i+1] if i+1 < len(sentences) else "."
            
            words = sentence.split()
            
            if len(words) <= max_length:
                result.append(sentence + punctuation)
            else:
                # Split into chunks
                for j in range(0, len(words), max_length):
                    chunk = " ".join(words[j:j+max_length])
                    result.append(chunk + ".")
        
        return " ".join(result)
    
    def _simplify_punctuation(self, text: str) -> str:
        """
        Simplify complex punctuation.
        
        Args:
            text: Text to process
            
        Returns:
            text with simplified punctuation
        """
        # Replace semicolons with periods
        text = text.replace(";", ".")
        # Replace multiple spaces
        text = re.sub(r'\s+', ' ', text)
        # Ensure sentences end properly
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        
        return text
    
    def _ensure_clarity(self, text: str) -> str:
        """
        Ensure text is clear and direct.
        
        Args:
            text: Text to process
            
        Returns:
            clearer text
        """
        # Remove redundant phrases
        text = re.sub(r'\bvery\s+very\b', 'very', text, flags=re.IGNORECASE)
        text = re.sub(r'\breally\s+really\b', 'really', text, flags=re.IGNORECASE)
        
        # Capitalize first letter
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
        
        return text

