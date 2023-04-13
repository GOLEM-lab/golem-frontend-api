from sparql import DB
from sparql_queries import CorpusMetrics, CorpusName, CorpusAcronym


class Corpus:
    """GOLEM Corpus

    Attributes:
        database (DB): Database Connection
        uri (str): URI of the corpus
        name (str) : Name of the corpus (an identifier)
        acronym (str) : Acronym of the corpus
        title (str) : Title of the corpus
        description (str) : Description of the corpus
        metrics (dict) : Metrics of a corpus
    """
    # Database connection
    database = None

    uri = None

    name = None

    acronym = None

    # Title of the Corpus
    title = None

    # Description of the Corpus
    description = None

    # Metrics of the corpus
    metrics = None

    def __init__(self, database: DB = None, uri: str = None, name: str = None, acronym: str = None):
        """

        Args:
            database: connection to a triple store. Use instance of class DB.
            uri (str): URI of the corpus
            name (str): Identifier (name) of the corpus

        """
        if database:
            self.database = database

        if uri:
            self.uri = uri

        if name:
            self.name = name
        else:
            # try to sparql the name from the knowledge graph
            try:
                self = self.get_name()
            except:
                pass

        if acronym:
            self.acronym = acronym

    def get_metrics(self, use_mapping: bool = False) -> dict:
        """Assemble and return corpus metrics.

         Uses a SPARQL Query of class "CorpusMetrics" of the module "sparql_queries".

        Args:
            use_mapping (bool): Use a mapping to transform the keys of the metrics dictionary. Defaults to False
        """

        if self.metrics:
            return metrics

        else:
            if self.database:
                if self.uri:
                    query = CorpusMetrics()
                    query.prepare()
                    query.inject([self.uri])
                    query.execute(self.database)
                    results = query.results.simplify()

                    metrics = dict()

                    if use_mapping:
                        # map the keys of the results of the SPARQL query; unfortunately, this has to be hardcoded here;
                        # Maybe the label could be included somewhere in the graph istead
                        """
                        'number_of_chapters': 700000,
                        'number_of_characters': 20,
                        'number_of_comments': 123,
                        'number_of_documents': 200000,
                        'number_of_female_characters': 8,
                        'number_of_nonbinary_characters': 2,
                        'number_of_paragraphs': 9000000,
                        'number_of_words-comments': 123000,
                        'number_of_words-text': 2000000000}
                        """
                        mapping = dict(
                            number_of_chapters="chapters",
                            number_of_characters="characters",
                            number_of_comments="comments",
                            number_of_documents="documents",
                            number_of_female_characters="female",
                            number_of_male_characters="male",
                            number_of_nonbinary_characters="nonbinary",
                            number_of_paragraphs="paragraphs"
                        )
                    else:
                        mapping = None

                    for item in results:
                        key_from_graph = item["dimensionURI"].split("/")[-1:][0]
                        if mapping:
                            if key_from_graph in mapping:
                                key = mapping[key_from_graph]
                            else:
                                key = key_from_graph
                        else:
                            key = key_from_graph
                        value = item["value"]
                        metrics[key] = value

                    self.metrics = metrics
                    return self.metrics

                else:
                    raise Exception("Can not retrieve data without Corpus URI. Set attribute uri first")
            else:
                raise Exception("Can not retrieve metrics without database connection.")

    def get_name(self) -> str:
        """Get name of a corpus.

        Uses SPARQL query "CorpusName" of the module "sparql_queries".
        """
        if self.name:
            return self.name
        else:
            if self.database:
                if self.uri:
                    query = CorpusName()
                    query.prepare()
                    query.inject([self.uri])
                    query.execute(self.database)
                    results = query.results.simplify()

                    if len(results) > 0:
                        self.name = results[0]
                        return self.name
                    else:
                        raise Exception("No name in the knowledge graph.")

                else:
                    raise Exception("URI of corpus is not set.")
            else:
                raise Exception("Can't retrieve name without database connection.")

    def get_acronym(self) -> str:
        """Get corpus acronym

        Uses SPARQL query "CorpusAcronym" of the module "sparql_queries".

        """
        if self.acronym:
            return self.acronym
        else:
            if self.database:
                if self.uri:
                    query = CorpusAcronym()
                    query.prepare()
                    query.inject([self.uri])
                    query.execute(self.database)
                    results = query.results.simplify()

                    if len(results) > 0:
                        self.acronym = results[0]
                        return self.acronym
                    else:
                        raise Exception("No acronym in the knowledge graph.")

                else:
                    raise Exception("URI of corpus is not set.")

            else:
                raise Exception("Can't retrieve acronym without database connection.")

    def get_metadata(self, include_metrics: bool = False) -> dict:
        """Serialize Corpus Metadata.

        Args:
            include_metrics (bool, optional): Include metrics. Defaults to False.

        Returns:
            dict: Serialization of the corpus metadata.
        """

        metadata = dict(
            uri=self.uri,
            name=self.name,
            title=self.title,
            description=self.description,
            acronym=self.get_acronym()
        )

        if include_metrics is True:
            # Use the hardcoded mappings by setting use_mapping to True
            metadata["metrics"] = self.get_metrics(use_mapping=True)

        return metadata
