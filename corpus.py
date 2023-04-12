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

    def get_metrics(self) -> dict:
        """Assemble and return corpus metrics.

         Uses a SPARQL Query of class "CorpusMetrics" of the module "sparql_queries".
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
                    for item in results:
                        key = item["dimensionURI"].split("/")[-1:][0]
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
            metadata["metrics"] = self.get_metrics()

        return metadata
