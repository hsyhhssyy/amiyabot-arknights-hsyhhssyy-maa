from datetime import datetime

from peewee import AutoField,CharField,TextField,DateTimeField

from amiyabot.database import ModelClass

from core.database.plugin import db

class AmiyaBotMAAConnection(ModelClass):
    id: int = AutoField()
    uuid: str = CharField()
    secret: str = CharField()
    signature: str = CharField()
    user_id: str = CharField(null=True)
    gui_json: str = TextField(null=True)

    class Meta:
        database = db
        table_name = "amiyabot-maa-connection"

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