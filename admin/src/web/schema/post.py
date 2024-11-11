from marshmallow import Schema, fields

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    author = fields.Str(required=True) # Mail from the user that made the post
    summary = fields.Str(required=True)
    state = fields.Str(required=True) # Preguntar si es con enum
    posted_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


post_schema = PostSchema()
posts_schema = PostSchema(many=True)

