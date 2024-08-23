from tortoise import Model, fields


class Share(Model):
    id = fields.IntField(pk=True)
    share_file_id = fields.CharField(max_length=255)
    filename = fields.CharField(max_length=255)
    extract_code = fields.CharField(max_length=255)
    expire_minutes = fields.IntField(default=30)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "share"
