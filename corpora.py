from corpus import Corpus


class Corpora:
    """Programmable Corpora

    Attributes:
        corpora (dict): Instances of class "Corpus" with "name" as keys.
        description (str): Description of the collection of corpora.
    """
    corpora = None
    description = None

    def __init__(self):
        pass

    def add_corpus(self, corpus: Corpus) -> bool:
        """Add a corpus.

        Stores a corpus in the class' attribute "corpora" with corpus.name as key.

        Args:
            corpus (Corpus): Instance of class "Corpus".

        Returns:
            bool: True if successful.
        """
        if corpus.name:
            self.corpora[corpus.name] = corpus
            return True

    def list_corpora(self, include_metrics: bool = False) -> list:
        """Get Metadata of corpora.

        Args:
            include_metrics (bool): Include metrics for each corpus. Defaults to False.

        Returns:
            list: Corpora.
        """
        corpus_list = list()
        if self.corpora:
            for corpus_name in self.corpora.keys():
                # this assumes, that a database connection is defined inside the corpus
                # TODO: handle the error of missing database connection
                corpus_item = self.corpora[corpus_name].get_metadata(include_metrics=include_metrics)
                corpus_list.append(corpus_item)
        return corpus_list

