import base64
import hmac
import json

from core import app
from amiyabot.network.httpServer import BaseModel

from ..server.check_password import get_password
from .database import AmiyaBotMAAConnectionModel

app.set_allow_path(['/maa/token'])

class GetTokenModel(BaseModel):
    uuid: str

class AuthModel(BaseModel):
    signature: str
    uuid: str

class ReportStatusModel(AuthModel):
    idle: bool


def validate_signature(model:AuthModel):
    signature = hmac.new(get_password().encode(), model.uuid, digestmod="SHA256").digest()
    if model.signature != signature:
        return False
    return True

@app.controller
class Maa:
    @app.route(method='get')
    async def token(self,data:GetTokenModel):
        signature = hmac.new(get_password().encode(), data.uuid, digestmod="SHA256").digest()

        AmiyaBotMAAConnectionModel.create(
            uuid = data.uuid,
            signature = signature
        )

        return app.response({"success":True,"code":signature})

    @app.route(method='post')
    async def get_task(self,data:AuthModel):        
        if not validate_signature(data):
            return app.response("invalid signature",401)

        return app.response({"success":True,"task":[]})
    
    @app.route(method='post')
    async def report_status(self,data:ReportStatusModel):        
        if not validate_signature(data):
            return app.response("invalid signature",401)

        return app.response({"success":True})
