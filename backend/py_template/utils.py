class Utils:
    @staticmethod
    def slug_to_title(slug):
        """
        Takes in hyphen-separated words in slugs,
        converts them to title case
        """
        prepositions = [
        "a", "an", "the","and", "but", "or", "for", "nor", "so", "yet",
        "at", "by", "in", "of", "on", "to", "up", "with", "from", "as"]
        words = slug.slug.split("-")
        words = [word if (word in prepositions and index != 0) else word.capitalize() for index,word in enumerate(words)]
        return " ".join(words)
