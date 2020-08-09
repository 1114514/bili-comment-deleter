#coding=utf-8

__author__ = 'bili__干冰不是冰'

'''
bilibili删评脚本, 仅供学习和研究.
'''

import asyncio
import aiohttp
import json
import random

oid=114514 # av号
ua='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.142 Safari/537.36' # 改成你自己的ua, 不改应该问题也不大
cookie='' # 填写你自己的cookie, 格式: 'a=b; c=d'
csrf='' # cookie中的bili_jct字段
get_url=f'https://api.bilibili.com/x/v2/reply?&type=1&pn=1&oid={oid}'
del_url='https://api.bilibili.com/x/v2/reply/del'

async def getCommentData(oid):
    global ua
    headers={
        'User-Agent':ua,
    }
    async with aiohttp.ClientSession(headers=headers) as session
        async with session.get(get_url) as resp:
            text = await resp.text()
            dic = json.loads(text)
            count = dic['data']['page']['count']
            print(f'status:{resp.status} comment_count:{count}')
            return count,dic

async def delComment(oid,rpid):
    global ua,cookie,csrf
    print('will delete rpid:',rpid)
    headers={
        'User-Agent':ua,
        'Cookie':cookie
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        postData={
            'oid': oid,
            'type': 1,
            'jsonp': 'jsonp',
            'rpid': rpid,
            'csrf': csrf,
        }
        async with session.post(del_url,data=postData) as resp:
            print('delete status',resp.status)
            text = await resp.text()

async def main():
    global oid
    c , _ = await getCommentData(oid)
    while True:
        await asyncio.sleep(4.5+random.random())
        count , data = await getCommentData(oid)
        if count > c :
            delCount = count - c
            tasks = []
            for comment in data['data']['replies'][:delCount]:
                task = delComment(oid,comment['rpid'])
                tasks.append(task)
            await asyncio.wait(tasks)

loop=asyncio.get_event_loop()
loop.run_until_complete(main())
