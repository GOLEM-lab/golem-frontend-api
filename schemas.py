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


class CorpusMetadata(Schema):
    """Schema of the corpus metadata"""
    name = fields.Str()
    uri = fields.Str()
    title = fields.Str()
    acronym = fields.Str()
    description = fields.Str()
    metrics = fields.Nested(CorpusMetrics, required=False)
    repository = fields.Str()