from datetime import datetime

from peewee import AutoField,CharField,IntegerField,DateTimeField

from amiyabot.database import ModelClass

from core import log
from core.database.plugin import PluginConfiguration

fields = {
    'id':  AutoField(),
    'uuid': CharField(),
    'secret': CharField(),
    'signature': CharField(),
    'user_id': CharField(null=True),
    'gui_json': CharField(null=True),
    'task': CharField(null=True)

}

def create_new_model(name, fields, base_model, table_name):
    # old_fields = base_model._meta.fields
    model_attrs = {k: v for k, v in fields.items()}
    model_attrs['Meta'] = type(
        'Meta', (), {'database': base_model._meta.database, 'table_name': table_name})
    new_model = type(name, (ModelClass,), model_attrs)
    return new_model


AmiyaBotMAAConnectionModel = create_new_model(
    'AmiyaBotMAAConnection', fields, PluginConfiguration,'amiyabot-maa-connection')
