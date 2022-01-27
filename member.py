import json
from urllib.parse import quote_plus
import requests
import logging
import re

logger = logging.getLogger(__name__)


class Member:
    def __init__(self, username, password, uid, link):
        self.is_login = False
        self.username = username
        self.password = password
        self.uid = uid
        self.link = link
        self.session = requests.Session()
        self.nickname = uid

    def login(self, on_success, on_failure):
        data = self.session.post(
            "https://bbs.saraba1st.com/2b/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1",
            data={"username": self.username, "password": self.password},
        ).text
        if "https://bbs.saraba1st.com/2b/./" in data:
            logger.info(self.username + ": 登陆成功")
            self.session.headers.update(
                {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Referer": "https://bbs.saraba1st.com/2b/forum-75-1.html",
                }
            )
            self.is_login = True
            on_success()
        else:
            logger.warning(data)
            on_failure()

    # 发请求保持在线
    def action(self):
        if not self.is_login:
            return
        data = self.session.get(
            'https://bbs.saraba1st.com/2b/home.php?mod=space&uid={}&do=profile&from=space'.format(self.uid)).text
        # 访问成功
        if "个人资料" in data:
            self.nickname = re.findall("<title>([^的]+)的个人资料", data)[0]
            last_visit = re.findall("最后访问<\/em>([^<]+)", data)[0]
            last_active = re.findall("上次活动时间<\/em>([^<]+)", data)[0]
            last_post = re.findall("上次发表时间<\/em>([^<]+)", data)[0]
            logger.info('最后访问={} 上次活动={} 上次发表={}'.format(
                last_visit, last_active, last_post))

            with open("config.json", "r") as f:
                config: list = json.load(f)
                try:
                    state = config["state"][self.uid]
                except:
                    state = {"last_visit": "",
                             "last_active": "", "last_post": ""}

            if last_visit != state["last_visit"]:
                self.notify("最后访问", state["last_visit"], last_visit)
            if last_active != state["last_active"]:
                self.notify("上次活动时间", state["last_active"], last_active)
            if last_post != state["last_post"]:
                self.notify("上次发表时间", state["last_post"], last_post)

            with open("config.json", "w") as f:
                if not "state" in config:
                    config["state"] = {}
                if not self.uid in config["state"]:
                    config["state"][self.uid] = {}
                config["state"][self.uid]["last_visit"] = last_visit
                config["state"][self.uid]["last_active"] = last_active
                config["state"][self.uid]["last_post"] = last_post

                json.dump(config, f, ensure_ascii=False, indent=2)

    def notify(self, tag, prev, new):
        self.session.get(self.link.format(quote_plus(
            "用户{}的{}由{}变为{}".format(self.nickname, tag, prev, new))))
