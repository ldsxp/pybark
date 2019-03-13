## 说明



**Bark 是什么**

[Bark](https://github.com/Finb/Bark) 是一款iOS应用程序，可让您将自定义通知推送到iPhone，支持链接和推送内容自动复制到剪切板。



**这又是什么**

这是 [Bark](https://github.com/Finb/Bark) 后端的 python 实现，参考 [go 版](https://github.com/Finb/bark-server) 和 [py-bark](https://github.com/billzhong/py-bark) 。可以方便 python 开发者集成到自己的服务器，还能用于本地消息的推送。



## 如何使用

### 创建虚拟环境

```sh
# 后面是注释
$ 是终端输入的内容，我习惯性的去掉它
```



```sh
#$ mkdir pybark
#$ cd pybark
# 在pybark根目录下运行
$ virtualenv .venv
# win
$ .venv\Scripts\activate
# linux 需要添加 source
# source .venv/bin/activate
$ pip install falcon apns2 shortuuid ilds
```



### 运行

```sh
python pybark\app.py
```



注：服务器运行的时候尽量用 gunicorn




## 用到的库



**falcon**

用于构建快速的Web API和应用程序后端

https://github.com/falconry/falcon

https://falcon.readthedocs.io

```
pip install falcon
```



**shortuuid**

简洁，明确且URL安全的UUID的生成器库

https://pypi.org/project/shortuuid/

https://github.com/skorokithakis/shortuuid

```
pip install shortuuid
```



**apns2**

Apple推送通知服务（APN）交互的Python库

https://pypi.org/project/apns2/

https://github.com/Pr0Ger/PyAPNs2

```
pip install apns2
```



**ilds**

常用模块的集合，为了多平台，多电脑调用方便

https://pypi.org/project/ilds

https://github.com/ldsxp/ilds

```sh
pip install ilds
```



### 推送证书:

- 当你需要集成Bark到自己的系统或重新实现后端代码时可能需要推送证书
  证书密码: bp
  有效期到: 2020-02-29
  [cert-20200229.p12](https://github.com/Finb/bark-server/releases/download/1.0.0/cert-20200229.p12)
- 请及时更新推送证书，证书过期前两个月会在[当前页面](https://day.app/2018/06/bark-server-document/)更新新的有效证书

**将p12文件转换为pem证书**

```sh
# 提示需要输入密码，输入导出 p12 时的密码
openssl pkcs12 -in ApnsCert.p12 -out ApnsCert.pem -nodes
```



### 其他:

1. APP端负责将[DeviceToken](https://developer.apple.com/documentation/uikit/uiapplicationdelegate/1622958-application)发送到服务端。 
   服务端收到一个推送请求后，将发送推送给Apple服务器。然后手机收到推送
2. 服务端代码: <https://github.com/Finb/go-tools/blob/master/Bark.go>
3. App代码: <https://github.com/Finb/Bark>

