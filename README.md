# HarukaBot-Red
 基于[HarukaBot](https://github.com/SK-415/HarukaBot)，适配Red协议

因[`go-cqhttp`停止维护](https://github.com/Mrs4s/go-cqhttp/issues/2471)，
且替代方案`chronocat`不支持`onebot`协议，故修改得到此版本，方便原`hb`用户迁移。

### 安装
```commandline
pip install haruka_bot_red
```

### 运行
```commandline
hb run
```

### 原hb用户如何迁移？
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