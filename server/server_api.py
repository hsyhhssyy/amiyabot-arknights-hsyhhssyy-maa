import base64
import hmac
import json

from core import app
from amiyabot.network.httpServer import BaseModel

from ..utils.logger import log

from ..server.check_password import get_password

from .database import AmiyaBotMAAConnectionModel

app.set_allow_path(['/maa/token','/maa/getTask','/maa/reportStatus','/maa/guiJson'])

class GetTokenModel(BaseModel):
    uuid: str
    secret:str

class AuthModel(BaseModel):
    signature: str
    uuid: str

class ReportStatusModel(AuthModel):
    status: str
    payload: str

class GuiJsonModel(AuthModel):
    gui_json: str

def validate_signature(model:AuthModel):

    connection = AmiyaBotMAAConnectionModel.get_or_none(AmiyaBotMAAConnectionModel.uuid == model.uuid)

    if connection is None:
        return None

    password = get_password().encode()

    log.info(f'{password},{connection.secret}')

    signature = hmac.new(password, connection.secret.encode(), digestmod="SHA256").digest()
    signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip("=")

    if model.signature != signature_encoded:
        return None
    return connection

@app.controller
class Maa:
    @app.route(method='post')
    async def token(self,data:GetTokenModel):
        
        password = get_password().encode()

        log.info(f'Token Aquire: {password},{data.secret}')

        signature = hmac.new(password, data.secret.encode(), digestmod="SHA256").digest()
        signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip("=")

        conn_check = AmiyaBotMAAConnectionModel.get_or_none(AmiyaBotMAAConnectionModel.uuid == data.uuid)
        if conn_check is not None:
            return app.response({"success":False,"reason":"uuid exists"})

        conn_check = AmiyaBotMAAConnectionModel.get_or_none(AmiyaBotMAAConnectionModel.signature == signature_encoded)
        if conn_check is not None:
            return app.response({"success":False,"reason":"secret exists"})

        AmiyaBotMAAConnectionModel.create(
            uuid = data.uuid,
            secret = data.secret,
            signature = signature_encoded
        )

        return app.response({"success":True,"code":signature_encoded})

    @app.route(method='post')
    async def get_task(self,data:AuthModel):        
        connection = validate_signature(data) 
        if connection is None:
            return app.response("invalid signature",401)

        if connection.task is None or connection.task == "":
            return app.response({"success":True,"task":[]})
        
        try:
            task = json.loads(connection.task)
        except Exception as e:
            return app.response({"success":True,"task":[]})

        return app.response({"success":True,"task":task["task_list"]})
    
    @app.route(method='post')
    async def report_status(self,data:ReportStatusModel):
        connection = validate_signature(data) 
        if connection is None:
            return app.response("invalid signature",401)

        if data.status == "COMPLETE":
            if connection.task is None or connection.task == "":
                return app.response({"success":True})
            
            try:
                task = json.loads(connection.task)
                task["task_list"] = [task for task in task["task_list"] if task["uuid"] != data.payload]
                
                if len(task["task_list"]) == 0:
                    connection.task = None
                    connection.save()
                else:
                    connection.task = json.dumps(task)
                    connection.save()

            except Exception as e:
                connection.task = None
                connection.save()
                return app.response({"success":True})

        return app.response({"success":True})
    
    @app.route(method='post')
    async def gui_json(self,data:GuiJsonModel):        
        connection = validate_signature(data) 
        if connection is None:
            return app.response("invalid signature",401)

        connection.gui_json = data.gui_json
        connection.save()

        return app.response({"success":True})

