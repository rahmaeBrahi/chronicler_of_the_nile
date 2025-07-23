import wikipedia
import re
from typing import List, Dict, Optional, Tuple

class WikipediaSearcher:
    """
    A utility class for searching and retrieving information from Wikipedia
    to enhance the Chronicler of the Nile's knowledge base.
    """
    
    def __init__(self, language='en'):
        """
        Initialize the Wikipedia searcher with a specific language.
        
        Args:
            language (str): Language code for Wikipedia (e.g., 'en', 'ar')
        """
        self.language = language
        wikipedia.set_lang(language)
        
    def set_language(self, language: str):
        """Set the Wikipedia language"""
        self.language = language
        wikipedia.set_lang(language)
        
    def search_topics(self, query: str, max_results: int = 5) -> List[str]:
        """
        Search for Wikipedia topics related to the query.
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results to return
            
        Returns:
            List[str]: List of Wikipedia page titles
        """
        try:
            print(f"🔍 Searching Wikipedia for: {query}")
            results = wikipedia.search(query, results=max_results)
            print(f"📋 Found {len(results)} results: {results}")
            return results
        except Exception as e:
            print(f"❌ Wikipedia search error: {e}")
            return []
    
    def get_page_summary(self, title: str, sentences: int = 3) -> Optional[str]:
        """
        Get a summary of a Wikipedia page.
        
        Args:
            title (str): Wikipedia page title
            sentences (int): Number of sentences to include in summary
            
        Returns:
            Optional[str]: Page summary or None if not found
        """
        try:
            print(f"📖 Getting summary for: {title}")
            summary = wikipedia.summary(title, sentences=sentences)
            print(f"✅ Summary retrieved: {len(summary)} characters")
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"🔀 Disambiguation page for '{title}', trying first option")
            if e.options:
                try:
                    return wikipedia.summary(e.options[0], sentences=sentences)
                except Exception as inner_e:
                    print(f"❌ Error with disambiguation option: {inner_e}")
                    return None
            return None
        except wikipedia.exceptions.PageError:
            print(f"❌ Page not found: {title}")
            return None
        except Exception as e:
            print(f"❌ Error getting summary for '{title}': {e}")
            return None
    
    def get_page_content(self, title: str, max_chars: int = 2000) -> Optional[str]:
        """
        Get the full content of a Wikipedia page (truncated).
        
        Args:
            title (str): Wikipedia page title
            max_chars (int): Maximum characters to return
            
        Returns:
            Optional[str]: Page content or None if not found
        """
        try:
            print(f"📄 Getting content for: {title}")
            page = wikipedia.page(title)
            content = page.content[:max_chars]
            if len(page.content) > max_chars:
                content += "..."
            print(f"✅ Content retrieved: {len(content)} characters")
            return content
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"🔀 Disambiguation page for '{title}', trying first option")
            if e.options:
                try:
                    page = wikipedia.page(e.options[0])
                    content = page.content[:max_chars]
                    if len(page.content) > max_chars:
                        content += "..."
                    return content
                except Exception as inner_e:
                    print(f"❌ Error with disambiguation option: {inner_e}")
                    return None
            return None
        except wikipedia.exceptions.PageError:
            print(f"❌ Page not found: {title}")
            return None
        except Exception as e:
            print(f"❌ Error getting content for '{title}': {e}")
            return None
    
    def search_egyptian_history(self, query: str) -> Dict[str, str]:
        """
        Search for Egyptian history-related topics and return relevant information.
        
        Args:
            query (str): Search query related to Egyptian history
            
        Returns:
            Dict[str, str]: Dictionary with topic titles as keys and summaries as values
        """
        print(f"🏺 Searching Egyptian history for: {query}")
        
        # Enhance query with Egyptian history keywords
        enhanced_queries = [
            query,
            f"{query} Egypt",
            f"{query} Egyptian",
            f"{query} ancient Egypt",
            f"{query} pharaoh",
            f"{query} Nile"
        ]
        
        results = {}
        seen_titles = set()
        
        for enhanced_query in enhanced_queries:
            try:
                search_results = self.search_topics(enhanced_query, max_results=3)
                
                for title in search_results:
                    if title.lower() in seen_titles:
                        continue
                    
                    seen_titles.add(title.lower())
                    
                    # Check if the title is related to Egypt/Egyptian history
                    if self._is_egyptian_related(title):
                        summary = self.get_page_summary(title, sentences=2)
                        if summary:
                            results[title] = summary
                            print(f"✅ Added Egyptian topic: {title}")
                    
                    # Limit total results
                    if len(results) >= 5:
                        break
                
                if len(results) >= 5:
                    break
                    
            except Exception as e:
                print(f"❌ Error in enhanced search for '{enhanced_query}': {e}")
                continue
        
        return results
    
    def _is_egyptian_related(self, title: str) -> bool:
        """
        Check if a Wikipedia title is related to Egyptian history.
        
        Args:
            title (str): Wikipedia page title
            
        Returns:
            bool: True if related to Egyptian history
        """
        egyptian_keywords = [
            'egypt', 'egyptian', 'pharaoh', 'pyramid', 'nile', 'cairo', 'alexandria',
            'cleopatra', 'tutankhamun', 'ramses', 'ptolemy', 'hieroglyph', 'sphinx',
            'luxor', 'karnak', 'thebes', 'memphis', 'giza', 'saqqara', 'abydos',
            'coptic', 'mamluk', 'fatimid', 'ayyubid', 'ottoman egypt', 'muhammad ali',
            'suez', 'aswan', 'nubia', 'kush', 'dynasty', 'kingdom egypt'
        ]
        
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in egyptian_keywords)
    
    def get_contextual_information(self, user_message: str, language: str = 'en') -> str:
        """
        Get contextual Wikipedia information based on user message.
        
        Args:
            user_message (str): User's message/question
            language (str): Language for search ('en' or 'ar')
            
        Returns:
            str: Formatted Wikipedia information to add to the prompt
        """
        print(f"🔍 Getting contextual information for: {user_message[:100]}...")
        
        # Set language for search
        original_lang = self.language
        if language != self.language:
            self.set_language(language)
        
        try:
            # Extract key terms from user message
            key_terms = self._extract_key_terms(user_message)
            print(f"🔑 Extracted key terms: {key_terms}")
            
            wikipedia_info = []
            
            for term in key_terms[:3]:  # Limit to top 3 terms
                if language == 'ar':
                    # For Arabic, search in English but provide context
                    self.set_language('en')
                    egyptian_results = self.search_egyptian_history(term)
                else:
                    egyptian_results = self.search_egyptian_history(term)
                
                for title, summary in egyptian_results.items():
                    wikipedia_info.append(f"**{title}**: {summary}")
                
                if len(wikipedia_info) >= 3:  # Limit total information
                    break
            
            # Format the information
            if wikipedia_info:
                formatted_info = "\n\n**Additional Context from Wikipedia:**\n" + "\n\n".join(wikipedia_info)
                print(f"✅ Retrieved {len(wikipedia_info)} pieces of contextual information")
                return formatted_info
            else:
                print("ℹ️ No relevant Wikipedia information found")
                return ""
                
        except Exception as e:
            print(f"❌ Error getting contextual information: {e}")
            return ""
        finally:
            # Restore original language
            if language != original_lang:
                self.set_language(original_lang)
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """
        Extract key terms from user message that might be relevant for Wikipedia search.
        
        Args:
            text (str): User message
            
        Returns:
            List[str]: List of key terms
        """
        # Remove common words and extract potential search terms
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'about', 'tell', 'me', 'what', 'how', 'when', 'where', 'why', 'who', 'which',
            'can', 'could', 'would', 'should', 'will', 'was', 'were', 'is', 'are', 'am', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'get', 'got', 'give',
            'أخبرني', 'عن', 'ما', 'هو', 'هي', 'كيف', 'متى', 'أين', 'لماذا', 'من', 'التي', 'الذي',
            'في', 'على', 'إلى', 'من', 'مع', 'عند', 'كان', 'كانت', 'يكون', 'تكون', 'هل', 'لا', 'نعم'
        }
        
        # Clean and split text
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out common words and short words
        key_terms = [word for word in words if len(word) > 2 and word not in common_words]
        
        # Also look for multi-word phrases that might be important
        phrases = []
        text_lower = text.lower()
        
        # Egyptian history specific terms
        egyptian_phrases = [
            'ancient egypt', 'old kingdom', 'middle kingdom', 'new kingdom', 'ptolemaic period',
            'roman egypt', 'islamic egypt', 'ottoman egypt', 'modern egypt', 'pharaonic period',
            'coptic period', 'mamluk period', 'fatimid period', 'ayyubid period',
            'مصر القديمة', 'الدولة القديمة', 'الدولة الوسطى', 'الدولة الحديثة', 'العصر البطلمي',
            'مصر الرومانية', 'مصر الإسلامية', 'مصر العثمانية', 'مصر الحديثة'
        ]
        
        for phrase in egyptian_phrases:
            if phrase in text_lower:
                phrases.append(phrase)
        
        # Combine single terms and phrases
        all_terms = key_terms + phrases
        
        # Remove duplicates and return top terms
        unique_terms = list(dict.fromkeys(all_terms))  # Preserves order
        return unique_terms[:5]  # Return top 5 terms

# Global instance for easy access
wikipedia_searcher = WikipediaSearcher()

