import os
import re
import uuid
import json
import asyncio

from datetime import datetime

from amiyabot import Message, Chain

from core.util import check_file_content
from core.customPluginInstance import AmiyaBotPluginInstance

from .server import server_api
from .server.server_api import external_adapters
from .utils.string_operation import extract_json, loads_or_none
from .utils.logger import log
from .server.database import AmiyaBotMAAConnection, AmiyaBotMAATask
from .server.check_password import is_strong_password

curr_dir = os.path.dirname(__file__)

data_dir = f"{curr_dir}/../../resource/maa-adapter"
if not os.path.exists(curr_dir):
    os.makedirs(curr_dir)

global_switch = True


class MaaAdapterPluginInstance(AmiyaBotPluginInstance):
    def install(self):
        AmiyaBotMAAConnection.create_table(safe=True)
        AmiyaBotMAATask.create_table(safe=True)
        log.bot = self

        if not is_strong_password():
            global global_switch
            global_switch = False
            log.info("警告：您的服务器秘钥设置的过于简单，出于安全考虑，不允许使用MAA连接器功能，请您修改您config/server.yaml中的连接秘钥，使其包含至少一个大写字母，一个小写字母，一个数字和一个特殊符号（!@#$%^&*(),.?:{}|<>）。")


bot = MaaAdapterPluginInstance(
    name='MAA对接器',
    version='2.0',
    plugin_id='amiyabot-arknights-hsyhhssyy-maa',
    plugin_type='',
    description='用于对接MAA',
    document=f'{curr_dir}/README.md',
    instruction=f'{curr_dir}/README_USE.md',
    global_config_default=f'{curr_dir}/configs/global_config_default.json',
    global_config_schema=f'{curr_dir}/configs/global_config_schema.json',

)


async def get_connection(data: Message):
    if not global_switch:
        await data.send(Chain(data).text('博士，该功能未开启。'))
        return False, None

    conn: AmiyaBotMAAConnection = AmiyaBotMAAConnection.get_or_none(
        AmiyaBotMAAConnection.user_id == data.user_id)

    if conn is None:
        await data.send(Chain(data).text('博士，您还没有绑定连接秘钥。'))
        return False, None

    if conn.validated == False:
        await data.send(Chain(data).text('博士，您还没有验证您的设备,请通过"记录MAA设备XXXXXXX"发送您的设备Id。'))
        return False, None

    return True, conn


@bot.on_message(keywords=['如何连接MAA'], level=5)
async def maa_start(data: Message):

    if not global_switch:
        return Chain(data, at=False).text('博士，该功能未开启。')

    conn_str = bot.get_config("connection_string").rstrip("/")

    if conn_str is None or conn_str == "":
        return Chain(data, at=False).text('博士，兔兔没有设置连接地址哦。')
    
    instStr =  f'获取任务端点是： {conn_str}/maa/getTask \n汇报任务端点是： {conn_str}/maa/reportStatus \n特制的Maa.exe下载地址是： https://github.com/hsyhhssyy/amiyabot-arknights-hsyhhssyy-maa/releases/'

    return Chain(data, at=False).markdown(check_file_content(f'{curr_dir}/README_USE.md')).text(instStr)


@bot.on_message(keywords=['记录MAA设备'], level=5)
async def maa_start(data: Message):

    if not global_switch:
        return Chain(data, at=False).text('博士，该功能未开启。')

    device_id = data.text.split("设备")[1] if "设备" in data.text else None
    # 判断该device是否未绑定，如果未绑定则进行绑定
    conn = AmiyaBotMAAConnection.get_or_none(
        AmiyaBotMAAConnection.device_id == device_id)

    if conn == None:
        return Chain(data, at=False).text('博士，系统还未记录到该设备ID，请您先去MAA配置或重新检查后再发哟。')

    if conn.user_id is not None and conn.user_id != data.user_id:
        return Chain(data, at=False).text('博士，该设备ID已经被其他用户使用。')
    
    conn.validated = True
    conn.save()

    return Chain(data, at=False).text(f'博士，该设备阿米娅记下了。')

def wait_snapshot(data,task_uuid):
    async def message_loop():
        while True:
            await asyncio.sleep(1)
            task = AmiyaBotMAATask.get(AmiyaBotMAATask.uuid == task_uuid)
            # log.info(f'{task.payload}')
            if task.payload is not None and task.payload != "":
                await data.send(Chain(data).text('博士，指挥终端返回了如下截图:').image(task.payload))
                return

    asyncio.create_task(message_loop())

def create_my_message_filter_lambda(original_data):
    return lambda data: data.user_id == original_data.user_id

@bot.on_message(keywords=['MAA截图'], level=5)
async def maa_fight(data: Message):

    valid, conn = await get_connection(data)

    if not valid:
        return

    task_uuid = str(uuid.uuid4())
    AmiyaBotMAATask.create(connection=conn.id, uuid=task_uuid, type="CaptureImage",
                           parameter=None, status="ASSIGNED", create_at=datetime.now())

    await data.send(Chain(data).text('博士，指挥终端当前任务结束后将发送截图给您。'))

    wait_snapshot(data,task_uuid)


@bot.on_message(keywords=['MAA立即截图'], level=5)
async def maa_fight(data: Message):

    valid, conn = await get_connection(data)
    if not valid:
        return

    task_uuid = str(uuid.uuid4())
    AmiyaBotMAATask.create(connection=conn.id, uuid=task_uuid, type="CaptureImageNow",
                           parameter=None, status="ASSIGNED", create_at=datetime.now())

    wait_snapshot(data,task_uuid)

@bot.on_message(keywords=['一键长草'], level=5)
async def maa_fight(data: Message):

    valid, conn = await get_connection(data)
    if not valid:
        return

    AmiyaBotMAATask.create(connection=conn.id, uuid=str(uuid.uuid4()), type="LinkStart",
                               parameter="", status="ASSIGNED", create_at=datetime.now())

    snapshot_task_uuid = str(uuid.uuid4())
    AmiyaBotMAATask.create(connection=conn.id, uuid=snapshot_task_uuid, type="CaptureImage",
                           parameter=None, status="ASSIGNED", create_at=datetime.now())

    wait_snapshot(data,snapshot_task_uuid)

    return Chain(data).text(f'博士，一键长草任务已布置，干员们会努力做好罗德岛的日常工作的，任务结束后将发送截图给您。')
