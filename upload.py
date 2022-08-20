import sys
import base64
import hashlib
import time
import requests
import urllib.parse
import os


def main():
    print(11)
    target = " http://120.25.218.79:9999"
    message = 'wdsjnswdwY0329&&19924519007@163.com'  # 自定义上传的信息,使服务端日志更清晰
    param = [urllib.parse.unquote(par, 'utf8') for par in sys.argv]  # 把url编码转换成中文
    param.__delitem__(0)  # 第一个参数是脚本文件本身
    if len(param) > 0:
        if not os.path.exists(param[0]):  # 通过判断第一个参数是不是文件来判断是否加了参数 ${filename}
            param.__delitem__(0)
        for i in range(0, len(param)):
            file = param[i]  # 不压缩图片
            with open(file, "rb") as f:
                content = base64.b64encode(f.read())
                filename = str(int(time.time())) + "_" + hashlib.md5(content).hexdigest() + param[i][
                                                                                            param[i].rfind('.'):]
                data = {'message': message, 'content': content, 'filename': filename}
                res = requests.post(target, data)
                if res.status_code == 200:
                    print(res.text)
                else:
                    print('Error uploading Gitee, please check')


if __name__ == '__main__':
    main()
