import os
import re
import uuid
import json
import asyncio

from datetime import datetime

from amiyabot import Message, Chain

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
    version='1.0',
    plugin_id='amiyabot-arknights-hsyhhssyy-maa',
    plugin_type='',
    description='用于对接MAA',
    document=f'{curr_dir}/README.md',
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

    if conn.gui_json is None or conn.gui_json == "":
        await data.send(Chain(data).text('博士，我还没有接收到来自您指挥终端的连接。'))
        return False, None

    return True, conn


@bot.on_message(keywords=['查看MAA连接地址'], level=5)
async def maa_start(data: Message):

    if not global_switch:
        return Chain(data, at=False).text('博士，该功能未开启。')

    conn_str = bot.get_config("connection_string")

    if conn_str is None or conn_str == "":
        return Chain(data, at=False).text('博士，兔兔没有设置连接地址哦。')
    return Chain(data, at=False).text(f'博士，连接地址是：{conn_str}')


@bot.on_message(keywords=['记录MAA密钥'], level=5)
async def maa_start(data: Message):

    if not global_switch:
        return Chain(data, at=False).text('博士，该功能未开启。')

    jsons = extract_json(data.text)
    if jsons is None or len(jsons) == 0:
        return Chain(data, at=False).text('博士，连接密钥格式不正确，请您重新检查后再发哟。')

    json = jsons[0]

    if "signature" in json.keys():
        signature = json["signature"]
        # 判断该Signature是否未绑定，如果未绑定则进行绑定
        conn = AmiyaBotMAAConnection.get_or_none(
            AmiyaBotMAAConnection.signature == signature)

        if conn == None:
            return Chain(data, at=False).text('博士，连接密钥格不匹配，请您重新检查后再发哟。')

        if conn.user_id is not None:
            return Chain(data, at=False).text('博士，该连接秘钥已经被绑定到其他用户上了哦。')

        AmiyaBotMAAConnection.delete().where(
            AmiyaBotMAAConnection.user_id == data.user_id).execute()

        conn.user_id = data.user_id
        conn.save()

    return Chain(data, at=False).text(f'博士，连接密钥阿米娅记下了。')

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

@bot.on_message(keywords=['MAA十连'], level=20)
async def maa_gacha(data: Message):

    valid, conn = await get_connection(data)

    if not valid:
        return


    confirm = await data.wait(Chain(data).text('博士，阿米娅即将通过指挥终端在当前活动寻访（寻访界面最左侧的寻访）中为您进行一次十连寻访。（该寻访为真实寻访），请您回复“确认”确认操作。'),
                              True,30)
    log.info(f'{confirm} {confirm.text}')
    if confirm is not None and confirm.text=='确认':
        await data.send(Chain(data).text('博士，十连抽任务已经下发'))
        AmiyaBotMAATask.create(connection=conn.id, uuid=str(uuid.uuid4()), type="Custom",
                            parameter=' {"task_names": [ "GachaTenTimes" ] }', status="ASSIGNED", create_at=datetime.now())
        
        task_uuid = str(uuid.uuid4())
        AmiyaBotMAATask.create(connection=conn.id, uuid=task_uuid, type="CaptureImage",
                            parameter=None, status="ASSIGNED", create_at=datetime.now())

        wait_snapshot(data,task_uuid)
    else:    
        await data.send(Chain(data).text('博士，十连抽任务已取消'))
    
    return

@bot.on_message(keywords=['MAA截图'], level=5)
async def maa_fight(data: Message):

    valid, conn = await get_connection(data)

    if not valid:
        return

    task_uuid = str(uuid.uuid4())
    AmiyaBotMAATask.create(connection=conn.id, uuid=task_uuid, type="CaptureImage",
                           parameter=None, status="ASSIGNED", create_at=datetime.now())

    await data.send(Chain(data).text('博士，指挥终端当前任务结束后将发送截图给您。'))

    async def message_loop():
        while True:
            await asyncio.sleep(1)
            task = AmiyaBotMAATask.get(AmiyaBotMAATask.uuid == task_uuid)
            # log.info(f'{task.payload}')
            if task.payload is not None and task.payload != "":
                await data.send(Chain(data).text('博士，指挥终端返回了如下截图:').image(task.payload))
                return

    asyncio.create_task(message_loop())


@bot.on_message(keywords=['MAA立即截图'], level=5)
async def maa_fight(data: Message):

    valid, conn = await get_connection(data)
    if not valid:
        return

    task_uuid = str(uuid.uuid4())
    AmiyaBotMAATask.create(connection=conn.id, uuid=task_uuid, type="CaptureImageNow",
                           parameter=None, status="ASSIGNED", create_at=datetime.now())

    async def message_loop():
        while True:
            await asyncio.sleep(1)
            task = AmiyaBotMAATask.get(AmiyaBotMAATask.uuid == task_uuid)
            # log.info(f'{task.payload}')
            if task.payload is not None and task.payload != "":
                await data.send(Chain(data).text('博士，指挥终端返回了如下截图:').image(task.payload))
                return

    asyncio.create_task(message_loop())


@bot.on_message(keywords=['MAA刷'], level=5)
async def maa_fight(data: Message):

    valid, conn = await get_connection(data)
    if not valid:
        return

    pattern = r"MAA刷(\d+)[把|次|关]([\s\S]*)"

    match = re.search(pattern, data.text_original)
    if match:
        num_of_times = match.group(1)
        stages = match.group(2)
        AmiyaBotMAATask.create(connection=conn.id, uuid=str(uuid.uuid4()), type="Fight",
                               parameter=json.dumps({
                                   "stage": stages,
                                   "times": int(num_of_times)
                               }), status="ASSIGNED", create_at=datetime.now())
        return Chain(data).text(f'博士，进行{num_of_times}次{stages}的战斗任务已经布置下去了，干员们会努力完成的。')

    return Chain(data).text(f'博士，您布置的任务阿米娅不明白。')


@bot.on_message(keywords=['MAA自动公招'], level=5)
async def maa_fight(data: Message):

    valid, conn = await get_connection(data)
    if not valid:
        return

    AmiyaBotMAATask.create(connection=conn.id, uuid=str(uuid.uuid4()), type="Recruit",
                           parameter=json.dumps({
                               "refresh": True,
                               "select": [3, 4, 5],
                               "confirm": [3, 4, 5],
                               "times": 4,
                               # "set_time": False,
                               # "expedite": False,
                               # "expedite_times": 0,
                               "skip_robot": False,
                               "recruitment_time": {
                                   "3": 540,
                                   "4": 540,
                                   "5": 540,
                               }
                           }), status="ASSIGNED", create_at=datetime.now())

    return Chain(data).text(f'博士，您布置的任务阿米娅不明白。')


@bot.on_message(keywords=['一键长草'], level=5)
async def maa_fight(data: Message):

    valid, conn = await get_connection(data)
    if not valid:
        return

    # 分析gui_json

    gui_json_obj: dict = loads_or_none(conn.gui_json)

    if gui_json_obj is None:
        log.info("gui.json的格式不正确，请检查您的maa的配置。")
        return Chain(data).text('博士，到指挥终端的连接不稳定，无法执行您的请求。')

    # 针对一键长草的每一个任务，添加一个task

    if gui_json_obj.get("TaskQueue.\u5F00\u59CB\u5524\u9192.IsChecked", None) == "True" or gui_json_obj.get("TaskQueue.WakeUp.IsChecked", None) == "True":
        # 开始唤醒
        AmiyaBotMAATask.create(connection=conn.id, uuid=str(uuid.uuid4()), type="StartUp",
                               parameter=None, status="ASSIGNED", create_at=datetime.now())

    if gui_json_obj.get("TaskQueue.\u81EA\u52A8\u516C\u62DB.IsChecked", None) == "True" or gui_json_obj.get("TaskQueue.Recruiting.IsChecked", None) == "True":
        # 开始唤醒
        select_list = []
        if bool(gui_json_obj.get("AutoRecruit.ChooseLevel3", True)) == True:
            select_list.append(3)
        if bool(gui_json_obj.get("AutoRecruit.ChooseLevel4", True)) == True:
            select_list.append(4)
        if bool(gui_json_obj.get("AutoRecruit.ChooseLevel5", True)) == True:
            select_list.append(5)

        AmiyaBotMAATask.create(connection=conn.id, uuid=str(uuid.uuid4()), type="Recruit",
                               parameter=json.dumps({
                                   "refresh": bool(gui_json_obj.get("AutoRecruit.RefreshLevel3", True)),
                                   "select": select_list,
                                   "confirm": select_list,
                                   "times": int(gui_json_obj.get("AutoRecruit.MaxTimes", 4)),
                                   # "set_time": False,
                                   # "expedite": False,
                                   # "expedite_times": 0,
                                   "skip_robot": bool(gui_json_obj.get("AutoRecruit.NotChooseLevel1", False)),
                                   "recruitment_time": {
                                       "3": 460 if bool(gui_json_obj.get("AutoRecruit.IsLevel3UseShortTime", False)) == True else 540,
                                       "4": 540,
                                       "5": 540,
                                   }
                               }), status="ASSIGNED", create_at=datetime.now())

    if gui_json_obj.get("TaskQueue.\u5237\u7406\u667A.IsChecked", None) == "True" or gui_json_obj.get("TaskQueue.Combat.IsChecked", None) == "True":
        AmiyaBotMAATask.create(connection=conn.id, uuid=str(uuid.uuid4()), type="Fight",
                               parameter=json.dumps({
                                   "stage": gui_json_obj.get("MainFunction.Stage1", "1-7"),
                                   "times": 99999
                               }), status="ASSIGNED", create_at=datetime.now())

    if gui_json_obj.get("TaskQueue.\u9886\u53D6\u65E5\u5E38\u5956\u52B1.IsChecked", None) == "True" or gui_json_obj.get("TaskQueue.Mission.IsChecked", None) == "True":
        AmiyaBotMAATask.create(connection=conn.id, uuid=str(uuid.uuid4()), type="Award",
                               parameter=None, status="ASSIGNED", create_at=datetime.now())

    return Chain(data).text(f'博士，任务已经布置下去了，干员们会努力做好罗德岛的日常工作的。')
