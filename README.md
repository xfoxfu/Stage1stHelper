# Stage1st 巨魔助手之观测器

**自动关注指定用户的最近访问情况，并且在发生变动的时候发送 Web HTTP GET 通知**

## 使用方法

1. 修改 config.json 中的配置，refresh_time 为每次刷新的时间间隔，测试过 300s 不会被离线。`watch` 中可以填入多个账号，可以按需要添加。

```json
{
  "refresh_time": 300,
  "watch": [
    {
      "username": "你的用户名",
      "password": "你的密码",
      "uid": "被观测者的UID",
      "link": "推送消息发送的HTTP地址，其中{}会被替换为通知消息（已经 URL 编码）"
    }
  ]
}
```

2. 执行 start.py。

```shell
python start.py
```

## 推送消息

推荐使用 [PushDeer](https://github.com/easychen/pushdeer)，推送消息地址可以填写为 `https://api2.pushdeer.com/message/push?pushkey=推送秘钥&text={}`。

或者可以使用 [Bark](https://github.com/Finb/Bark)，推送消息地址可以填写为 `https://api.day.app/推送秘钥/{}?level=passive`。
