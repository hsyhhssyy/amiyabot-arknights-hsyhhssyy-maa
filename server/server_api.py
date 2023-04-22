from core import app

from amiyabot.network.httpServer import BaseModel
from ..utils.native_jwt import get_jwt,check_jwt

app.set_allow_path(['/maa/token'])

class GetTokenModel(BaseModel):
    uuid: str

class AuthModel(BaseModel):
    jwt: str
    uuid: str

class ReportStatusModel(AuthModel):
    idle: bool


def validate_jwt(model:AuthModel):
    return check_jwt(model.jwt,model.uuid)

@app.controller
class Maa:
    @app.route(method='get')
    async def token(self,data:GetTokenModel):

        jwt =  get_jwt(data.uuid)

        return app.response({"success":True,"jwt":jwt})

    @app.route(method='post')
    async def get_task(self,data:AuthModel):
        
        if not validate_jwt(data):
            return app.response("invalid jwt",401)


        return app.response({"success":True,"task":[]})
    
    @app.route(method='post')
    async def report_status(self,data:ReportStatusModel):
        
        if not validate_jwt(data):
            return app.response("invalid jwt",401)

        return app.response({"success":True})
