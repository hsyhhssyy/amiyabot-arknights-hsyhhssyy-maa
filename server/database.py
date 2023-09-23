from datetime import datetime

from peewee import AutoField,CharField,TextField,DateTimeField,BooleanField

from amiyabot.database import ModelClass

from core.database.plugin import db

class AmiyaBotMAAConnection(ModelClass):
    id: int = AutoField()
    device_id: str = CharField()
    user_id: str = CharField()
    validated: bool = BooleanField()

    class Meta:
        database = db
        table_name = "amiyabot-maa-connection-new"

class AmiyaBotMAATask(ModelClass):
    id: int = AutoField()
    connection: str = CharField()
    uuid: str = CharField()
    type: str = CharField()
    parameter: str = TextField(null=True)
    status: str = CharField(null=True)
    payload: str = TextField(null=True)
    create_at: datetime = DateTimeField(null=True)
    update_at: datetime = DateTimeField(null=True)

    class Meta:
        database = db
        table_name = "amiyabot-maa-task"