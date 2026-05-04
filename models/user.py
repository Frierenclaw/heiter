from tortoise import models, fields

class User(models.Model):
    id = fields.UUIDField(pk=True)

    username = fields.CharField(max_length=256, unique=True)
    password = fields.BinaryField() # bcrypt password

    