from datetime import datetime

from peewee import AutoField,CharField,IntegerField,DateTimeField

from core import log
from core.database.plugin import PluginConfiguration

fields = {
    'id':  AutoField(),
    'user_id': CharField(),
    'token': CharField(null=True),
    'sercrt': CharField()
}


def create_new_model(name, fields, base_model,table_name):
    model_attrs = {k: v for k, v in fields.items()}
    model_attrs['Meta'] = type(
        'Meta', (), {'database': base_model._meta.database,'table_name':table_name})
    new_model = type(name, (base_model,), model_attrs)
    return new_model


AmiyaBotMAAConnectionModel = create_new_model(
    'AmiyaBotMAAConnection', fields, PluginConfiguration,'amiyabot-maa-connection')
