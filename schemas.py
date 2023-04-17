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


class ExternalReference(Schema):
    """Item in External Reference Ressource"""
    ref = fields.Str()
    type = fields.Str()


class Author(Schema):
    """Metadata on a single author"""
    id = fields.Str()
    uri = fields.Str() # maybe should add that
    authorName = fields.Str()
    refs = fields.Nested(ExternalReference)


class Character(Schema):
    """Metadata on a single character"""
    id = fields.Str()
    uri = fields.Str() # would add that
    characterName = fields.Str()
    entryName = fields.Str()
    refs = fields.Nested(ExternalReference, required=False)
    source = fields.Str() # Maybe sourceName
    sourceUrl = fields.Str
    createdYear = fields.Int()
    firstFanficYear = fields.Int()
    numDocuments = fields.Int()
    networkdataCsvUrl = fields.Str()
    authors = fields.Nested(Author)


class Corpus(Schema):
    """Schema of the corpus.
    """
    id = fields.Str()
    uri = fields.Str()
    corpusName = fields.Str()
    acronym = fields.Str()
    description = fields.Str(required=False)
    licence = fields.Str()
    licenceUrl = fields.Str()
    repository = fields.Str(required=False)
    metrics = fields.Nested(CorpusMetrics, required=False)
    characters = fields.Nested(Character, required=False)
