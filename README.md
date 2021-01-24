# light-uniquebots
UniqueBots를 위한 길드수 업뎃만 하는 모듈.

## 기능
서버수 자동 업데이트  
**이 외의 기능은 추가할 생각이 없습니다**

## 설치
```
pip install light-uniquebots
```

## 예제
```py
import light_uniquebots as lub
import discord

client = discord.Client()
ubot_token = "uniquebots_token"
lub_client = lub.LUBClient(bot=client, token=ubot_token)

client.run("discord_token")
```