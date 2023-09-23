import os
import base64

from peewee import SelectQuery
from datetime import datetime, timedelta

from core import app

from amiyabot.network.httpServer import BaseModel

from ..utils.logger import log

from ..server.check_password import get_password

from .database import AmiyaBotMAAConnection, AmiyaBotMAATask

app.set_allow_path(['/maa/reportStatus','/maa/getTask'])

class AuthModel(BaseModel):
    user: str
    device: str

class ReportStatusModel(AuthModel):
    status: str
    task: str
    payload: str

external_adapters = {}


curr_dir = os.path.dirname(__file__)
screenshot_dir = f"{curr_dir}/../../../resource/maa-adapter/screenshots"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

@app.controller
class Maa:
    @app.route(method='post')
    async def get_task(self, data: AuthModel):
        connection = AmiyaBotMAAConnection.get_or_none(
            (AmiyaBotMAAConnection.device_id == data.device)&(AmiyaBotMAAConnection.user_id == data.user))

        if connection is None:
            connection = AmiyaBotMAAConnection.create(device_id=data.device,user_id=data.user,validated=False)

        tasks = []

        if connection.validated == False:
            return app.response({"success": False, "tasks": tasks})

        # 查询task
        query: SelectQuery = (AmiyaBotMAATask
                              .select()
                              .where((AmiyaBotMAATask.connection == connection.id)
                                     & (AmiyaBotMAATask.status == "ASSIGNED") & (AmiyaBotMAATask.create_at > datetime.now() - timedelta(minutes=15))))

        for task in query:  # type: AmiyaBotMAATask
            task_to_append = {
                "id": task.uuid,
                "type": task.type,
                "params": task.parameter
            }
            tasks.append(task_to_append)

        return {"success": True, "tasks": tasks}

    @app.route(method='post')
    async def report_status(self, data: ReportStatusModel):
        connection = AmiyaBotMAAConnection.get_or_none(
            (AmiyaBotMAAConnection.device_id == data.device)&(AmiyaBotMAAConnection.user_id == data.user))
        
        if connection is None or connection.validated == False:
            return app.response("invalid uid/did", 401)

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

        return {"success": True}