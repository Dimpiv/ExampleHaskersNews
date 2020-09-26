"""
Example parser first 30 posts from Hacker News
"""

import asyncio
from abc import ABC
import aiohttp
from bs4 import BeautifulSoup
from aiohttp import web
from src.model import SqlTool


class Parser(BeautifulSoup, ABC):
    """Parsing web methods"""

    def __init__(self, html):
        super().__init__(html, "html.parser")
        self.base = SqlTool()

    def set_titles(self):
        """Save to database titles and urls from remote server"""
        result = list()
        main_table = self.find("table", "itemlist")
        for title in main_table.find_all("a", "storylink"):
            result.append(dict(title=title.text, url=title.get("href")))
        self.base.add_posts(result)


class Spider:
    """The main class that implements the reception and return of data by api"""

    def __init__(self, url: str):
        self.url = url
        self.page = str()
        self.base = SqlTool()
        self.app = web.Application()
        self.app.add_routes([web.get('/posts', self.get_posts),
                             web.get('/update', self.update_posts)])

    def save_posts(self):
        pars = Parser(self.page)
        pars.set_titles()

    async def parse_posts(self):
        """Get and Parse posts from remote server and save to DataBase"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    self.page = await response.text()
                    self.save_posts()
        except Exception as err:
            print(err)

    async def update_posts(self, _):
        """Update posts from remote server"""
        await self.parse_posts()
        return web.json_response(dict(message="Updated!"))

    async def get_posts(self, request):
        """
        Send saved posts from DataBase
        params:
            ?limit = (int) number of posts returned
        """
        limit = request.query.get('limit', 5)
        try:
            limit = int(limit)
            if limit < 0:
                limit = limit * -1
        except Exception as err:
            print(err)
            return web.json_response(dict(error="Invalid parameter limit"))
        return web.json_response(self.base.get_posts(limit))


if __name__ == '__main__':
    client = Spider(url="https://news.ycombinator.com/")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.parse_posts())
    web.run_app(client.app, host="0.0.0.0", port=8000)
