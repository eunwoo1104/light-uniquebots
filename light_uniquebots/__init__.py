"""
MIT License

Copyright (c) 2021 eunwoo1104

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import aiohttp
import asyncio
import logging

__version__ = "1.0.0"


class LUBClient:
    """
    light_uniquebots의 클라이언트입니다.
    모든 인자들은 keyword 형태로 전달되어야 합니다.
    :param bot: `discord.Client` 또는 `discord.ext.commands.Bot` 또는 이 두개 중에서 하나를 상속받은 클래스이어야 합니다.
    :param token: str. UniqueBots 토큰입니다.
    :param loop: asyncio 이벤트 루프입니다. 꼭 넣을 필요는 없습니다. 기본값은 discord.py의 이벤트 루프 입니다.
    :param run_update: bool. 만약에 `False`일 경우 업데이트 태스크가 생성되지 않습니다. 기본값은 True 입니다.
    """
    base_url = "https://uniquebots.kr/graphql"

    def __init__(self, *, bot, token, loop=None, run_update: bool = True):
        self.bot = bot
        self.__token = token if token.startswith("Bot ") else f"Bot {token}"
        self.loop = loop or self.bot.loop
        self.logger = logging.getLogger('light-uniquebots')
        self.before = 0
        if run_update:
            self.loop.create_task(self.__update())

    async def update(self):
        """
        UniqueBots에 길드 카운트를 업데이트하는 코루틴 함수입니다.
        """
        self.logger.debug("Posting guild count now...")
        if self.before == len(self.bot.guilds):
            self.logger.debug("Same guild count. Canceled.")
            return
        header = {"Authorization": self.__token}
        body = {"query": """query{bot(id:"me"){guilds(patch:__COUNT__)}}""".replace("__COUNT__", str(len(self.bot.guilds)))}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, headers=header, json=body) as resp:
                ret = await resp.json()
                if "errors" not in ret:
                    self.before = len(self.bot.guilds)
                    self.logger.info("Guild count post success.")
                elif resp.status == 429:
                    self.logger.debug("Rate limited, skipping.")
                else:
                    self.logger.error(f"Failed guild post count. Errors: `{', `'.join([x['message'] for x in ret['errors']])}`")

    async def __update(self):
        await self.bot.wait_for("ready")
        header = {"Authorization": self.__token}
        body = {"query": """query{bot(id:"me"){guilds}}"""}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, headers=header, json=body) as resp:
                ret = await resp.json()
        if "errors" in ret:
            self.logger.error(f"Failed getting guild count from UniqueBots; Guild count update canceled.\n"
                              f"Errors: `{', `'.join([x['message'] for x in ret['errors']])}`")
            return
        self.before = int(ret["data"]["bot"]["guilds"])
        self.logger.debug(f"Got guild count from UniqueBots: {self.before}")
        while not self.bot.is_closed():
            await self.update()
            await asyncio.sleep(60)
