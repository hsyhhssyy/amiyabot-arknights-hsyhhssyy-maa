import os
import re
import uuid
import json

from amiyabot import Message, Chain


from core.customPluginInstance import AmiyaBotPluginInstance

from .server import server_api
from .utils.string_operation import extract_json
from .utils.logger import log
from .server.database import AmiyaBotMAAConnectionModel
from .server.check_password import is_strong_password

curr_dir = os.path.dirname(__file__)

global_switch = True

class MaaAdapterPluginInstance(AmiyaBotPluginInstance):
    def install(self):
        AmiyaBotMAAConnectionModel.create_table(safe=True)
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

@bot.on_message(keywords=['查看MAA连接地址'], level=5)
async def maa_start(data: Message):

    if not global_switch:
        return Chain(data,at=False).text('博士，该功能未开启。')
    
    conn_str = bot.get_config("connection_string")

    if conn_str is None or conn_str == "":
        return Chain(data,at=False).text('博士，兔兔没有设置连接地址哦。')
    return Chain(data,at=False).text(f'博士，连接地址是：{conn_str}')


@bot.on_message(keywords=['记录MAA密钥'], level=5)
async def maa_start(data: Message):    

    if not global_switch:
        return Chain(data,at=False).text('博士，该功能未开启。')

    jsons = extract_json(data.text)    
    if jsons is None or len(jsons)==0:
        return Chain(data,at=False).text('博士，连接密钥格式不正确，请您重新检查后再发哟。')

    json = jsons[0]

    if "signature" in json.keys():
        signature = json["signature"]
        # 判断该Signature是否未绑定，如果未绑定则进行绑定
        conn = AmiyaBotMAAConnectionModel.get_or_none(AmiyaBotMAAConnectionModel.signature == signature)

        if conn == None:
            return Chain(data,at=False).text('博士，连接密钥格不匹配，请您重新检查后再发哟。')
        
        if conn.user_id is not None:
            return Chain(data,at=False).text('博士，该连接秘钥已经被绑定到其他用户上了哦。')
        
        conn = AmiyaBotMAAConnectionModel.delete.where(AmiyaBotMAAConnectionModel.user_id == data.user_id).execute()

        conn.user_id = data.user_id
        conn.save()

    return Chain(data,at=False).text(f'博士，连接密钥阿米娅记下了。')

@bot.on_message(keywords=['MAA刷'], level=5)
async def maa_fight(data: Message):

    if not global_switch:
        return Chain(data,at=False).text('博士，该功能未开启。')

    conn = AmiyaBotMAAConnectionModel.get_or_none(AmiyaBotMAAConnectionModel.user_id == data.user_id)

    if conn is None:
        return Chain(data).text('博士，您还没有绑定连接秘钥。')
    
    if conn.task is not None and conn.task != "":
        return Chain(data).text('博士，上一个任务还在执行中。')
    
    task = {
        "task_list":[
            {
                "uuid":str(uuid.uuid4()),
                "type":"Fight",
                "parameter": json.dumps({
                    "stage":"1-7",
                    "times":1
                })
            }
        ]
    }

    conn.task = json.dumps(task)
    conn.save()

    return Chain(data).text('博士，任务已经下发。')

