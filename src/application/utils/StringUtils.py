import re


class StringUtils():
    
    @staticmethod
    def count_text(word: str, text: str) -> int:
        """
        Count the number of occurrences of a word in a text

        Args:
            word (str): Word to search for
            text (str): Text to search in

        Returns:
            int: Number of occurrences
        """
        
        return word.lower().count(text.lower())
    
    @staticmethod
    def regex_match(regex: str, text: str) -> bool:
        """
        Check if a regex matches a text

        Args:
            regex (str): Regular expression
            text (str): Text to search in

        Returns:
            bool: True if matches, False otherwise
        """
        
        pattern = re.compile(regex, re.IGNORECASE)
        return bool(pattern.search(text))