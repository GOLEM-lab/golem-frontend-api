from marshmallow import Schema, fields


class ApiInfo(Schema):
    """Schema of the response of the 'api/info' endpoint"""
    name = fields.Str()
    version = fields.Str()
    description = fields.Str()


class WordCount(Schema):
    """Schema of the wordcount included in CorpusMetrics"""
    words_in_documents = fields.Int()
    words_in_comments = fields.Int()


class CorpusMetrics(Schema):
    """Schema of the corpus metrics included in the corpus metadata"""
    documents = fields.Int()
    chapters = fields.Int()
    paragraphs = fields.Int()
    characters = fields.Int()
    male = fields.Int()
    female = fields.Int()
    nonbinary = fields.Int()
    comments = fields.Int()
    wordcount = fields.Nested(WordCount, required=True)


# TODO: maybe merge schemas Corpus and CorpusMetadata with the one below; use optional fields
class CorpusMetadata(Schema):
    """Schema of the corpus metadata

    Included in the response of the /corpora endpoint
    """
    name = fields.Str()
    uri = fields.Str()
    title = fields.Str()
    acronym = fields.Str()
    description = fields.Str()
    metrics = fields.Nested(CorpusMetrics, required=False)
    repository = fields.Str()


class ExternalReference(Schema):
    """Item in External Reference Ressource"""
    ref = fields.Str()
    type = fields.Str()


class Author(Schema):
    """Metadata on a single author"""
    id = fields.Str()
    uri = fields.Str() # maybe should add that
    authorName = fields.Str()
    authorFullname = fields.Str()
    authorShortname = fields.Str()
    refs = fields.Nested(ExternalReference)


class Character(Schema):
    """Metadata on a single character"""
    id = fields.Str()
    uri = fields.Str() # would add that
    characterName = fields.Str()
    entryName = fields.Str()
    wikidataId = fields.Str() # Maybe harmonize with author (refs)?
    source = fields.Str() # Maybe sourceName
    sourceUrl = fields.Str
    createdYear = fields.Int()
    firstFanficYear = fields.Int()
    numDocuments = fields.Int()
    networkdataCsvUrl = fields.Str()
    authors = fields.Nested(Author)


class Corpus(Schema):
    """Schema of the corpus.

    Returned by the /corpora/{corpusname} endpoint
    """
    name = fields.Str()
    uri = fields.Str()
    title = fields.Str()
    licence = fields.Str()
    licenceUrl = fields.Str()
    repository = fields.Str()
    characters = fields.Nested(Character)

