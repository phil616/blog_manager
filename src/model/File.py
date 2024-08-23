from tortoise import Model, fields


class File(Model):
    fid = fields.CharField(max_length=100, unique=True)
    filename = fields.CharField(max_length=255)
    mimetype = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "file"
