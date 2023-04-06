class Corpus:
    """Corpus

    Attributes:
        name (str): Name of the corpus. To be used as an ID.
        title (str): Title of the corpus.
        description (str): Description of the corpus.

    """
    # Corpus Name. An ID somehow.
    name = None

    # Title of the Corpus
    title = None

    # Description of the Corpus
    description = None

    def __init__(self,
                 name: str = None,
                 title: str = None,
                 description: str = None):
        """Initialize corpus

        Args:
            name (str, optional): Name (ID) of the corpus.
            title (str, optional): Title of the corpus.
            description (str, optional): Description.
        """

        if name:
            self.name = name

        if title:
            self.title = title

        if description:
            self.description = description



