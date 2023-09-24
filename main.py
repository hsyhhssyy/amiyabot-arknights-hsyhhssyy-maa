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
                await data.send(Chain(data).text('博士，任务完成了。指挥终端返回了如下截图:').image(task.payload))
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

async def assign_simple_task_with_snapshot(data,maa_type,mission_str):
    
    valid, conn = await get_connection(data)
    if not valid:
        return

    AmiyaBotMAATask.create(connection=conn.id, uuid=str(uuid.uuid4()), type=maa_type,
                               parameter="", status="ASSIGNED", create_at=datetime.now())

    snapshot_task_uuid = str(uuid.uuid4())
    AmiyaBotMAATask.create(connection=conn.id, uuid=snapshot_task_uuid, type="CaptureImage",
                           parameter=None, status="ASSIGNED", create_at=datetime.now())

    wait_snapshot(data,snapshot_task_uuid)

    return Chain(data).text(f'博士，{mission_str}任务已布置，干员们会努力做好罗德岛的日常工作的，任务结束后将发送截图给您。')

@bot.on_message(keywords=['MAA一键长草'], level=5)
async def maa_fight(data: Message):
    return await assign_simple_task_with_snapshot(data,"LinkStart","一键长草")

@bot.on_message(keywords=['MAA基建换班'], level=5)
async def maa_fight(data: Message):
    return await assign_simple_task_with_snapshot(data,"LinkStart-Base","基建换班")

@bot.on_message(keywords=['MAA开始唤醒'], level=5)
async def maa_fight(data: Message):
    return await assign_simple_task_with_snapshot(data,"LinkStart-WakeUp","开始唤醒")

@bot.on_message(keywords=['MAA刷理智'], level=5)
async def maa_fight(data: Message):
    return await assign_simple_task_with_snapshot(data,"LinkStart-Combat","战斗")

@bot.on_message(keywords=['MAA自动公招'], level=999)
async def maa_fight(data: Message):
    return await assign_simple_task_with_snapshot(data,"LinkStart-Recruiting","公开招募")

@bot.on_message(keywords=['MAA获取信用及购物'], level=5)
async def maa_fight(data: Message):
    return await assign_simple_task_with_snapshot(data,"LinkStart-Mall","购物")

@bot.on_message(keywords=['MAA领取奖励'], level=5)
async def maa_fight(data: Message):
    return await assign_simple_task_with_snapshot(data,"LinkStart-Mission","领取奖励")

@bot.on_message(keywords=['MAA自动肉鸽'], level=5)
async def maa_fight(data: Message):
    return await assign_simple_task_with_snapshot(data,"LinkStart-AutoRoguelike","集成战略")

@bot.on_message(keywords=['MAA生息演算'], level=5)
async def maa_fight(data: Message):
    return await assign_simple_task_with_snapshot(data,"LinkStart-ReclamationAlgorithm","生息演算")

@bot.on_message(keywords=['MAA十连抽'], level=20)
async def maa_gacha(data: Message):

    valid, conn = await get_connection(data)

    if not valid:
        return

    confirm = await data.wait(Chain(data).text('博士，阿米娅即将通过指挥终端在当前活动寻访（寻访界面最左侧的寻访）中为您执行寻访十次。（该寻访为真实寻访），请您回复“确认”确认操作。'),
                              True,30)
    log.info(f'{confirm} {confirm.text}')
    if confirm is not None and confirm.text=='确认':
        await data.send(Chain(data).text('博士，寻访十次任务已经下发'))
        AmiyaBotMAATask.create(connection=conn.id, uuid=str(uuid.uuid4()), type="Toolbox-GachaTenTimes",
                            parameter="", status="ASSIGNED", create_at=datetime.now())
        
        task_uuid = str(uuid.uuid4())
        AmiyaBotMAATask.create(connection=conn.id, uuid=task_uuid, type="CaptureImage",
                            parameter=None, status="ASSIGNED", create_at=datetime.now())

        wait_snapshot(data,task_uuid)
    else:    
        await data.send(Chain(data).text('博士，寻访十次任务已取消'))
    
    return

@bot.on_message(keywords=['MAA单抽'], level=20)
async def maa_gacha(data: Message):

    valid, conn = await get_connection(data)

    if not valid:
        return

    confirm = await data.wait(Chain(data).text('博士，阿米娅即将通过指挥终端在当前活动寻访（寻访界面最左侧的寻访）中为您进行一次寻访。（该寻访为真实寻访），请您回复“确认”确认操作。'),
                              True,30)
    log.info(f'{confirm} {confirm.text}')
    if confirm is not None and confirm.text=='确认':
        await data.send(Chain(data).text('博士，单次寻访任务已经下发'))
        AmiyaBotMAATask.create(connection=conn.id, uuid=str(uuid.uuid4()), type="Toolbox-GachaOnce",
                            parameter="", status="ASSIGNED", create_at=datetime.now())
        
        task_uuid = str(uuid.uuid4())
        AmiyaBotMAATask.create(connection=conn.id, uuid=task_uuid, type="CaptureImage",
                            parameter=None, status="ASSIGNED", create_at=datetime.now())

        wait_snapshot(data,task_uuid)
    else:    
        await data.send(Chain(data).text('博士，单次寻访任务已取消'))
    
    return