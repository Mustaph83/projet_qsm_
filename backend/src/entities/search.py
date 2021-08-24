from marshmallow import Schema, fields


class SearchSchema(Schema):
    number = fields.Str()
    startTime = fields.Str()
    stopTime = fields.Str()