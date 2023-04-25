# 兔兔与MAA对接器

1. 安装了该插件以后，配套使用我开发的WPF MAA被控端，可以实现通过兔兔聊天控制MAA。
2. 每个群友需要自己启动模拟器和安装配置MAA以及被控端。
3. 兔兔部署者则需要提供一个公网域名或者IP，以供群友的被控端连接。
4. 安装该插件后，插件会检查你的链接密钥，就是连接Console填写的那个，如果这个密钥强度不够，则不允许使用本功能。这是为了防止兔兔被暴露到公网后，出现各种安全隐患。密钥要求必须要有一个大写字母，一个小写字母，一个数字和一个特殊符号，并且要8位以上。
5. 小提示：请检查你的公网网关诸如Nginx配置是否允许超过10M的文件上传，上传截图很大的。

![例子](https://raw.githubusercontent.com/hsyhhssyy/amiyabot-arknights-hsyhhssyy-maa/master/docs/example.png)

## 如何使用

我是兔兔管理员

1. 首先您需要到控制台的设置页面填入您的公网ip地址和域名，就像填写在控制台里的那样。
2. 然后，然后就完事了，剩下的就交给兔兔。
3. 有条件的话，建议最好去Github上下载被控端exe并放到群文件里，因为Github有些地方的人可能打不开。

 [被控端下载地址](https://github.com/hsyhhssyy/amiyabot-maa-adapter/releases/tag/v.0.0.3)

我是兔兔的群友

1. 你需要一个已经配置好的MAA WPF GUI，确定能用它连接模拟器并配置好了各项功能。至少配置好一键长草并确定可以执行。具体流程请参照MAA的教程。
2. 下载被控端并打开，如果MAA需要管理员启动，则本程序也要管理员启动。
3. 将MAA所在文件夹填入第一步的文本框。或者点击浏览按钮并找到MaaCore.dll
4. 联系兔兔的管理员，管他要连接地址，填到第二步连接地址文本框里，或者如果管理员配置了兔兔，在群聊中说`兔兔查看MAA连接地址`，兔兔会回复你。
3. 按下生成密钥按钮，然后复制密钥文本框里的密钥，然后到群里，说`兔兔记录MAA密钥<密钥内容>`让兔兔记住密钥。不必担心其他人看到密钥，他们就算复制了这个密钥也没用。

    ![记住密钥](https://raw.githubusercontent.com/hsyhhssyy/amiyabot-arknights-hsyhhssyy-maa/master/docs/remember_secret.jpg)

4. 接下来就是挂机，然后去群聊里和兔兔聊天吧。记得停止MAA的任务，本程序不能和MAA同时开启并控制同一个模拟器。如果你更换了兔兔链接地址，记得重新生成密钥并发给兔兔。

## 兔兔支持的命令

|  命令   | 说明  | 引入版本  |
|  ----  | ----  | ----  | 
| 兔兔MAA一键长草  | 执行MMA的一键长草功能 | 1.0 |
| 兔兔MAA刷5次1-7 | 执行MMA的战斗刷图功能，注意：不会碎石和吃理智药 | 1.0 |
| 兔兔MAA自动公招 | 立刻执行一轮公招 | 1.0 |
| 兔兔MAA截图 | 截图，但是要在当前任务执行完毕后才会返回给你 | 1.0 |
| 兔兔MAA立即截图 | 程序一旦有机会就立即截图 | 1.0 |

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