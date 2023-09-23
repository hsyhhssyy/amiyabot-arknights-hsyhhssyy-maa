# 兔兔与MAA对接器

**<span style="color:red;">财产损失警告！MAA控制的是你真实的明日方舟账户。尽管MAA的开发者和本插件的开发者尽了最大努力，但是程序开发不可避免的存在Bug。因此，对于使用MAA，以及本插件，所造成的的财产损失，本插件的开发者，以及MAA的开发者概不负责。</span>**

**和MAA的对接需要大量测试！希望各位用户和开发者，能够尽可能多在Github上提Issue，不管是提交Bug，还是推荐新的功能。（不过我只有每天晚上有时间写代码呜呜呜）**

## 更新提示

2.0版本起，不再使用独立开发的被控端，转而使用一个特制的WindowsWPF版MAA客户端。用来防止各种各样的连接问题。

**新旧插件不兼容！**如果你发现新版本有问题，并且旧版本可以使用，你可以先暂时使用旧版插件以及旧版被控端。

现在，再连不上模拟器，就去找玛丽报Bug吧:-)

## 这是什么

1. 安装了该插件以后，使用一个特殊版本的MAA，可以实现通过兔兔聊天控制MAA。
2. 每个群友需要自己启动模拟器和安装配置MAA。
3. 兔兔部署者则需要提供一个公网域名或者IP，以供群友的被控端连接。
4. 安装该插件后，插件会检查你的链接密钥，就是连接Console填写的那个，**如果这个密钥强度不够，则不允许使用本功能**。这是为了防止兔兔被暴露到公网后，出现各种安全隐患。密钥要求必须要有一个大写字母，一个小写字母，一个数字和一个特殊符号，并且要8位以上。
5. 小提示：请检查你的公网网关诸如Nginx配置是否允许超过10M的文件上传，上传截图很大的。

![例子](https://raw.githubusercontent.com/hsyhhssyy/amiyabot-arknights-hsyhhssyy-maa/master/docs/usage_example.png)

## 什么是MAA

如果你还不知道，MAA 的意思是 MAA Assistant Arknights

一款明日方舟游戏小助手

基于图像识别技术，一键完成全部日常任务！

如果你还不知道MAA的话，快去下面的链接看看吧。

[快去给玛丽点赞把](https://github.com/MaaAssistantArknights/MaaAssistantArknights)


## 如何使用

我是兔兔管理员

1. 首先您需要到控制台的设置页面填入您的公网ip地址和域名，就像填写在控制台里的那样。
2. 然后，然后就完事了，剩下的就交给兔兔。
3. 有条件的话，建议最好去Github上下载这个特制的MAA.exe并放到群文件里，因为Github有些地方的人可能打不开。

 [特制MAA下载地址](https://github.com/hsyhhssyy/amiyabot-arknights-hsyhhssyy-maa/releases/)

我是兔兔的群友

1. 你需要下载特殊版本的MAA.exe文件并用它替换MAA文件夹下的对应文件。
2. 启动这个特制的MAA，确定能用它连接模拟器并配置好了各项功能。至少配置好一键长草并确定可以执行。具体流程请参照MAA的教程。
3. 打开MAA的设置，进入“远程控制”，在用户标识符中填入你的QQ号。
4. 如果设备标识符为空，按一下旁边的重新生成按钮，生成一个。
5. 在群聊中说`兔兔如何连接MAA`，兔兔会回复你要填写的地址。
6. 将兔兔说的地址，填写到MAA中`远程控制`设置的`获取任务端点`和`汇报任务端点`文本框里
7. 复制设备标识符，然后到群里，说`兔兔记录MAA设备<设备标识符>`让兔兔记住。不必担心其他人看到，他们就算复制了这个标识符也没用。

    ![记住密钥](https://raw.githubusercontent.com/hsyhhssyy/amiyabot-arknights-hsyhhssyy-maa/master/docs/remember_did.png)

8. 接下来就是挂机，然后去群聊里和兔兔聊天吧。

## 兔兔支持的命令

|  命令   | 说明  | 引入版本  |
|  ----  | ----  | ----  | 
| 兔兔MAA一键长草  | 执行MMA的一键长草功能，等效于按下主界面的LinkStart | 1.0 |
| 兔兔MAA截图 | 在当前所有任务执行完毕后截图并返回给你，可以用于帮你了解任务什么时候执行完。 | 1.0 |

截图存储在resource/maa-adapter/screenshots文件夹下，请注意定时清理。

更多命令请等待后续推出。

## 鸣谢

> [插件项目地址:Github](https://github.com/hsyhhssyy/amiyabot-arknights-hsyhhssyy-maa/)

> [被控端项目地址:Github](https://github.com/hsyhhssyy/amiyabot-maa-adapter/)

> [遇到问题可以在这里反馈(Github)](https://github.com/hsyhhssyy/amiyabot-arknights-hsyhhssyy-maa/issues/new/)

> [如果上面的连接无法打开可以在这里反馈(Gitee)](https://gitee.com/hsyhhssyy/amiyabot-plugin-bug-report/issues/new)

> [Logo作者:Sesern老师](https://space.bilibili.com/305550122)

|  版本   | 变更  |
|  ----  | ----  |
| 1.0  | 内部测试版本 |
| 1.1  | 提高了功能函数的优先级防止被公招功能覆盖，现在一键长草会说出下发的具体任务 |
| 1.2  | 修改了检测秘钥的代码,输出更友好的信息 |