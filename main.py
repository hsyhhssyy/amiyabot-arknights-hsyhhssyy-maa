import os
import re

from amiyabot import Message, Chain, log

from core.customPluginInstance import AmiyaBotPluginInstance

from .server import server_api
from .utils.string_operation import extract_json

curr_dir = os.path.dirname(__file__)

class MaaAdapterPluginInstance(AmiyaBotPluginInstance):
    def install(self):
       pass


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
    
    conn_str = bot.get_config("connection_string")

    if conn_str is None or conn_str == "":
        return Chain(data,at=False).text('博士，兔兔没有设置连接地址哦。')
    return Chain(data,at=False).text(f'博士，连接地址是：{conn_str}')


@bot.on_message(keywords=['记录MAA密钥'], level=5)
async def maa_start(data: Message):
    
    json = extract_json(data.text)
    
    if json is None:
        return Chain(data,at=False).text('博士，连接密钥格式不正确，请您重新检查后再发哟。')

    

    return Chain(data,at=False).text(f'博士，连接密钥阿米娅记下了。')