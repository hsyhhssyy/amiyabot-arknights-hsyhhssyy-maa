import base64
import hmac
import os

from peewee import SelectQuery
from datetime import datetime

from core import app

from amiyabot.network.httpServer import BaseModel

from ..utils.logger import log

from ..server.check_password import get_password

from .database import AmiyaBotMAAConnection, AmiyaBotMAATask

app.set_allow_path(['/maa/token','/maa/login', '/maa/getTask',
                   '/maa/reportStatus', '/maa/guiJson'])


class GetTokenModel(BaseModel):
    uuid: str
    secret: str


class AuthModel(BaseModel):
    signature: str
    uuid: str


class ReportStatusModel(AuthModel):
    status: str
    task: str
    payload: str


class GuiJsonModel(AuthModel):
    gui_json: str

def validate_signature(model: AuthModel):

    connection = AmiyaBotMAAConnection.get_or_none(
        AmiyaBotMAAConnection.uuid == model.uuid)

    if connection is None:
        return None

    password = get_password().encode()

    log.info(f'token verify:{connection.secret}')

    signature = hmac.new(password, connection.secret.encode(),
                         digestmod="SHA256").digest()
    signature_encoded = base64.urlsafe_b64encode(
        signature).decode().rstrip("=")

    if model.signature != signature_encoded:
        return None
    return connection


external_adapters = {}


curr_dir = os.path.dirname(__file__)
screenshot_dir = f"{curr_dir}/../../../resource/maa-adapter/screenshots"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

@app.controller
class Maa:
    @app.route(method='post')
    async def token(self, data: GetTokenModel):

        password = get_password().encode()

        log.info(f'Token Aquire: {data.secret}')

        signature = hmac.new(password, data.secret.encode(),
                             digestmod="SHA256").digest()
        signature_encoded = base64.urlsafe_b64encode(
            signature).decode().rstrip("=")

        conn_check = AmiyaBotMAAConnection.get_or_none(
            AmiyaBotMAAConnection.uuid == data.uuid)
        if conn_check is not None:
            return app.response({"success": False, "reason": "uuid exists"})

        conn_check = AmiyaBotMAAConnection.get_or_none(
            AmiyaBotMAAConnection.signature == signature_encoded)
        if conn_check is not None:
            return app.response({"success": False, "reason": "secret exists"})

        AmiyaBotMAAConnection.create(
            uuid=data.uuid,
            secret=data.secret,
            signature=signature_encoded
        )

        return app.response({"success": True, "code": signature_encoded})

    @app.route(method='post')
    async def login(self, data: AuthModel):

        connection = validate_signature(data)
        if connection is None:
            return app.response("invalid signature", 401)

        return app.response({"success": True})

    @app.route(method='post')
    async def get_task(self, data: AuthModel):
        connection = validate_signature(data)
        if connection is None:
            return app.response("invalid signature", 401)

        # 查询task
        query: SelectQuery = (AmiyaBotMAATask
                              .select()
                              .where((AmiyaBotMAATask.connection == connection.id)
                                     & (AmiyaBotMAATask.status == "ASSIGNED")))

        tasks = []

        for task in query:  # type: AmiyaBotMAATask
            task_to_append = {
                "uuid": task.uuid,
                "type": task.type,
                "parameter": task.parameter
            }
            tasks.append(task_to_append)

        return app.response({"success": True, "task": tasks})

    @app.route(method='post')
    async def report_status(self, data: ReportStatusModel):
        connection = validate_signature(data)
        if connection is None:
            return app.response("invalid signature", 401)

        task : AmiyaBotMAATask = AmiyaBotMAATask.get_or_none(
            AmiyaBotMAATask.uuid == data.task, AmiyaBotMAATask.connection == connection.id)

        if task is None:
            return app.response({"success": False})

        task.status = data.status
        task.update_at = datetime.now()

        if task.type == "CaptureImage" or task.type == "CaptureImageNow":
            with open(f'{screenshot_dir}/{task.uuid}.png', 'wb') as f:
                f.write(base64.b64decode(data.payload))
            task.payload = f'{screenshot_dir}/{task.uuid}.png'
            log.info(f'{task.payload}')

        task.save()

        return app.response({"success": True})

    @app.route(method='post')
    async def gui_json(self, data: GuiJsonModel):
        connection = validate_signature(data)
        if connection is None:
            return app.response("invalid signature", 401)

        connection.gui_json = data.gui_json
        connection.save()

        return app.response({"success": True})
