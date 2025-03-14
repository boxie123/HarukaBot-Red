# HarukaBot-Red

> **归档说明**
> 
> QQ限制了较旧版本客户端登录，同时在较新版客户端增加了针对llqqnt的检测，导致账号会不定时下线，暂时无解决方法。
>
> 由于本项目->`chronocat`->llqqnt的强依赖链，在llqqnt有解决方法之前，本项目暂时归档。

 基于[HarukaBot](https://github.com/SK-415/HarukaBot)，适配Red协议

因[`go-cqhttp`停止维护](https://github.com/Mrs4s/go-cqhttp/issues/2471)，
且替代方案`chronocat`不支持`onebot`协议，故修改得到此版本，方便原`hb`用户迁移。

## 须知
**`chronocat`目前虽然仍在持续维护，~但并未开源~已恢复[开源](https://github.com/chrononeko/chronocat)，如果你是新用户，更推荐继续使用原版[`HarukaBot`](https://github.com/SK-415/HarukaBot)配合[`Shamrock`](https://github.com/whitechi73/OpenShamrock)(有封号风险)或[`LiteLoaderQQNT-OneBotApi`](https://github.com/linyuchen/LiteLoaderQQNT-OneBotApi)，而非本项目。**

## 使用

### 安装
```commandline
pip install haruka_bot_red
```

### 运行
```commandline
hb run
```

### 原hb用户如何迁移？

> [!TIP]
> 如果你是新用户，或许并不需要以下内容

1. 卸载原环境中的`haruka_bot`，或新建虚拟环境，并安装`haruka_bot_red`
1. 在原`.env.prod`中添加行：
    ```dotenv
    DRIVER=~fastapi+~httpx+~websockets
    RED_AUTO_DETECT=True
    ```
1. 运行
    ```commandline
    hb run
    ```

### 相比原`HarukaBot`有何区别？
1. 适配`Red`协议而非`Onebot`, 可与`chronocat`链接；
2. 添加配置项`HARUKA_BROWSER_UA`和`HARUKA_BROWSER_COOKIE`, 用户可自行配置, 大幅降低风控概率;
3. 使用`Restful Api`爬取动态列表，相比`gRPC`接口更稳定，更新频率低;
4. 删除自动同意好友申请功能；


> README完善中，点个star为作者加速
