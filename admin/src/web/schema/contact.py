from marshmallow import Schema, fields

class ContactSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    message = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    captcha = fields.Str(required=True)


contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)
create_contact_schema = ContactSchema(only=('name', 'last_name', 'email', 'message', 'captcha'))