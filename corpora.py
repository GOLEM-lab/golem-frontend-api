from corpus import Corpus
from sparql import DB
from sparql_queries import CorporaUris


class Corpora:
    """Programmable Corpora (adapted for GOLEM Project)

    Attributes:
        corpora (dict): Instances of class "Corpus" with "name" as keys.
        description (str): Description of the collection of corpora.
        database (DB): Triple Store connection of class DB.
        uris (list): List of URIs of corpora.
    """
    corpora = None

    description = """Corpora contained in GOLEM's Knowledge Graph."""

    database = None

    uris = None

    def __init__(self,
                 corpora: dict = None,
                 description: str = None,
                 database: DB = None,
                 uris: list = None):
        """Initialize Corpora

        Args:
            corpora (dict): Instances of class "Corpus" with name as keys.
            description (str): Description of the collection of corpora.
            database (DB): Triple Store connection of class DB.
            uris (list): List of URIs of corpora.
        """

        if corpora:
            self.corpora = corpora

        if database:
            self.database = database

        # if corpora a passed and a global database is set, add this database to each corpus, if it does not have any
        if database and self.corpora:
            for corpus_name in self.corpora.keys():
                if self.corpora[corpus_name].database:
                    pass
                else:
                    # set the global database for this corpus
                    self.corpora[corpus_name].database = self.database

        if description:
            self.description = description

        if uris:
            self.uris = uris

    def get_uris(self):
        """Get URIs of Corpora in the Knowledge Graph

        Uses a SPARQL Query of class "CorporaUris" of the module "sparql_queries".

        """
        if self.uris:
            return self.uris
        else:
            if self.database:
                query = CorporaUris()
                query.prepare()
                query.execute(self.database)
                self.uris = query.results.simplify()
                return self.uris

            else:
                raise Exception("Can not retrieve uris without database connection.")

    def add_corpus(self, corpus: Corpus) -> bool:
        """Add a corpus instance.

        Stores a corpus (instance of class Corpus) in the class' attribute "corpora" with corpus.name as key.

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

