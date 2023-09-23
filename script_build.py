import sys
import os
import re

amiya_bot_plugin_paths = [
    "/mnt/amiya-bot/2912336120/plugins",
    "/mnt/amiya-bot/2604475967/plugins"
]

command = sys.argv[1]

if command != "build" and command != "test":
    print("请使用build或者test命令")
    exit()


if command == "test":
    if len(sys.argv) < 3:
        print("请使用test命令，然后输入一个数字参数")
        exit()

    amiya_bot_plugin_paths = [
        "/mnt/amiya-bot/2912336120/plugins",
        "/mnt/amiya-bot/2604475967/plugins"
    ]

    index = int(sys.argv[2])-1

    if index >= len(amiya_bot_plugin_paths):
        print("请输入正确的数字参数，范围为1到{}".format(len(amiya_bot_plugin_paths)))
        exit()

    amiya_bot_plugin_path = amiya_bot_plugin_paths[index]
else:
    amiya_bot_plugin_path = None

def read_file(file_name):
    # 获取当前脚本所在的目录
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    # 将目录和文件名组合成文件路径
    file_path = os.path.join(curr_dir, file_name)

    # 检查文件是否存在
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    else:
        print(f"文件 '{file_name}' 不存在.")
        return None

file_name = 'main.py'
content = read_file(file_name)

if not content:
    print('未找到main.py')

version_pattern = r"version='([\d.]+)'"
plugin_id_pattern = r"plugin_id='([\w-]+)'"

version_match = re.search(version_pattern, content)
plugin_id_match = re.search(plugin_id_pattern, content)

if not version_match or not plugin_id_match:
    print('未找到main.py下的配置项')
    exit

version = version_match.group(1)
plugin_id = plugin_id_match.group(1)

if command=="build":
    os.system(f'rm {plugin_id}-*.zip')
    os.system(f'zip -q -r {plugin_id}-{version}.zip *')
else:
    os.system(f'sudo rm {plugin_id}-*.zip')
    os.system(f'zip -q -r {plugin_id}-{version}.zip *')
    os.system(f'sudo rm -rf {amiya_bot_plugin_path}/{plugin_id}-*')
    os.system(f'cp {plugin_id}-*.zip {amiya_bot_plugin_path}/')

    # 如果您是docker请用这一句
    # os.system(f'docker restart amiya-bot')

    # 下面这句是在kubernetes下，重新创建指定dep下的所有pod
    app_names = [
        "amiya-bot-1-deployment",
        "amiya-bot-2-deployment"
    ]

    app_name = app_names[index]

    namespace_name = "amiya-bot"

    # 获取指定Deployment的所有Pod
    get_pods_command = f"kubectl get pods -l app={app_name} -n {namespace_name} -o jsonpath='{{.items[*].metadata.name}}'"

    # 使用os.system执行命令并获取所有Pod的名称
    pods = os.popen(get_pods_command).read().split()

    # 遍历Pod列表并删除每个Pod
    for pod in pods:
        delete_pod_command = f"kubectl delete pod -n {namespace_name} {pod}"
        os.system(delete_pod_command)
        print(f"Deleted pod: {pod}")

    print("All pods have been deleted. Kubernetes will recreate the pods.")
    

