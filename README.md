# 兔兔与MAA对接器

**<span style="color:red;">财产损失警告！MAA控制的是你真实的明日方舟账户。尽管MAA的开发者和本插件的开发者尽了最大努力，但是程序开发不可避免的存在Bug。因此，对于使用MAA，以及本插件，所造成的的财产损失，本插件的开发者，以及MAA的开发者概不负责。</span>**

**<span style="color:green;">喜报！远程控制功能已经正式加入官方MAA，从最新版的v4.25.0开始，可以直接使用官方MAA对接此插件进行控制。</span>**

**和MAA的对接需要大量测试！希望各位用户和开发者，能够尽可能多在Github上提Issue，不管是提交Bug，还是推荐新的功能。（不过我只有每天晚上有时间写代码呜呜呜）**

如果你发现MAA在远控时执行逻辑有问题，比如说“执行完十连抽后执行基建排班会导致页面卡死，因为基建排班功能不能从抽卡页面起始。”这样的bug，也请汇报给我，让我修改兔兔插件的任务下发逻辑，比如在基建排班之前插入一个唤醒，或者调整MAA的相关代码之类的。

## 更新提示

2.0版本起，将直接使用MAA的远程控制功能。**新旧插件不兼容！**，因为MAA已经正式支持远控，建议所有用户放弃旧版插件。
现在，再连不上模拟器，就去找玛丽报Bug吧:-)

2.2版本加入了切换连接地址的命令。

## 这是什么

1. 安装了该插件以后，可以实现通过兔兔聊天控制MAA。
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

[快去给玛丽点赞吧](https://github.com/MaaAssistantArknights/MaaAssistantArknights)


## 如何使用

我是兔兔管理员

1. 首先您需要到控制台的设置页面填入您的公网ip地址和域名，就像填写在控制台里的那样。
2. 然后，然后就完事了，剩下的就交给兔兔。

**<span style="color:red;">注意，目前版本的兔兔，Web服务启动时，有可能会出现顺序异常导致服务不生效，具体表现为有人访问/maa/getTask或/maa/reportStatus时报告404NotFound，兔兔会在未来版本修复此问题。目前遇到时请重启兔兔，还不行的话多重启几次就会好，一旦没问题了，只要兔兔不关闭，就不会再出问题。</span>**

我是兔兔的群友

1. 首先你需要下载安装一个MAA，目前仅支持Windows版本的MAA。
2. 启动MAA，确定能用它连接模拟器并配置好了各项功能。至少配置好一键长草并确定可以执行。具体流程请参照MAA的教程。
3. 打开MAA的设置，进入“远程控制”，在用户标识符中填入你的QQ号。
4. 如果设备标识符为空，按一下旁边的重新生成按钮，生成一个。
5. 在群聊中说`兔兔如何连接MAA`，兔兔会回复你要填写的地址。
6. 将兔兔说的地址，填写到MAA中`远程控制`设置的`获取任务端点`和`汇报任务端点`文本框里
7. 复制设备标识符，然后到群里，说`兔兔记录MAA设备<设备标识符>`让兔兔记住。不必担心其他人看到，他们就算复制了这个标识符也没用。

![记住密钥](https://raw.githubusercontent.com/hsyhhssyy/amiyabot-arknights-hsyhhssyy-maa/master/docs/remember_did.png)

8. 接下来就是挂机，然后去群聊里和兔兔聊天吧。

## 兔兔支持的命令

### 独立功能:

|  命令   | 说明  | 引入版本  |
|  ----  | ----  | ----  | 
| 兔兔MAA一键长草  | 执行MMA的一键长草功能，等效于按下主界面的LinkStart | 1.0 |
| 兔兔MAA截图 | 在当前所有任务执行完毕后截图并返回给你，可以用于帮你了解任务什么时候执行完。 | 1.0 |

### 一键长草子功能

下面的功能相当于单独执行一键长草中的对应子功能，不过会无视主界面上的勾选框。也就是说哪怕你没有勾选自动肉鸽，你也可以发送`兔兔MAA自动肉鸽`。
各个项目的配置遵循一键长草中的配置。

|  命令   | 说明  | 引入版本  |
|  ----  | ----  | ----  | 
| 兔兔MAA基建换班 | 无 | 2.1 |
| 兔兔MAA开始唤醒 | 无，这个功能好像没啥用 | 2.1 |
| 兔兔MAA刷理智 | 无 | 2.1 |
| 兔兔MAA自动公招 | 无 | 2.1 |
| 兔兔MAA获取信用及购物 | 无 | 2.1 |
| 兔兔MAA领取奖励 | 无 | 2.1 |
| 兔兔MAA自动肉鸽 | 记得去高级设置里，把执行次数调小不然任务停不下来 | 2.1 |
| 兔兔MAA生息演算 | 因为活动未开所以未测试！ | 2.1 |

### 小工具子功能

|  命令   | 说明  | 引入版本  |
|  ----  | ----  | ----  | 
| 兔兔MAA十连抽 | 进行一次十连抽（这是真实抽卡！） | 2.1 |
| 兔兔MAA单抽 | 进行一次单抽（这是真实抽卡！） | 2.1 |

### 修改配置子功能

|  命令   | 说明  | 引入版本  |
|  ----  | ----  | ----  | 
| 兔兔MAA切换连接地址emulator-5554 | 修改`设置->连接设置->连接地址`配置项的值，可用于切换模拟器。使用时连接地址紧跟在命令后。 | 2.2 |

**任务会按顺序执行，如果你下发了一个无限持续的任务（比如刷999999把肉鸽），那你后续的指令都不会生效了。**

截图存储在resource/maa-adapter/screenshots文件夹下，请注意定时清理。

更多命令请等待后续推出。

## 我也想做一个控制端

现在可以去看MAA的[官方开发文档](
https://maa.plus/docs/3.8-%E8%BF%9C%E7%A8%8B%E6%8E%A7%E5%88%B6%E5%8D%8F%E8%AE%AE.html)来了解如何开发控制端了。


## 鸣谢

> [插件项目地址:Github](https://github.com/hsyhhssyy/amiyabot-arknights-hsyhhssyy-maa/)

> [遇到问题可以在这里反馈(Github)](https://github.com/hsyhhssyy/amiyabot-arknights-hsyhhssyy-maa/issues/new/)

> [如果上面的连接无法打开可以在这里反馈(Gitee)](https://gitee.com/hsyhhssyy/amiyabot-plugin-bug-report/issues/new)

> Logo作者: Stable-Diffusion

|  版本   | 变更  |
|  ----  | ----  |
| 1.0  | 内部测试版本 |
| 1.1  | 提高了功能函数的优先级防止被公招功能覆盖，现在一键长草会说出下发的具体任务 |
| 1.2  | 修改了检测秘钥的代码,输出更友好的信息 |
| 2.0  | 大幅修改并使用MAA自身来进行远控 |
| 2.1  | 增加功能，并提供针对官方版MAA的说明 |
| 2.2  | 增加功能 |
| 2.3  | 适配新版兔兔 |