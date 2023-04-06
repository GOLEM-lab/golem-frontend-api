from sparql import DB
from corpora import Corpora
from golem_corpus import GolemCorpus
from sparql_queries import CorporaUris


class GolemCorpora(Corpora):
    """GOLEM Project's corpora.

    Attributes:
        database (DB): Database connection of class "DB" of the sparql module.
    """
    corpora = None

    description = """Corpora contained in GOLEM's Knowledge Graph."""

    database = None

    uris = None

    def __init__(self, database: DB = None):
        # add the database connection to each corpus if no database connection is explicitly defined in the corpus

        if database:
            self.database = database

        if database and self.corpora:
            for corpus_name in self.corpora.keys():
                if self.corpora[corpus_name].database:
                    pass
                else:
                    # set the global database for this corpus
                    self.corpora[corpus_name].database = database

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
                raise Exception("Can not retrieve metrics without database connection.")
