import time
import discord
import requests
from discord.ext import commands
import json
from discord import Embed
from discord.utils import get


intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

intercom_token = "dG9rOjgyNWRjZjg0XzFhZjVfNDI1M19iZDM3X2E4ZGM5NmI1MTYwYzoxOjA="

# При запуске бота устанавливается статус

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name="World Of Warcraft"))
  print('We have logged in as {0.user}'.format(client))

# При входе клиента на сервер постится сообщение
@client.event
async def on_member_join(member):
  # Создание эмбеда
  embed = Embed(
    title="Welcome to PlayCarry Boosting Services!",
    url="https://playcarry.com/",
    description=f"Hi, {member.mention}! \n This server is a DM server to communicate with our support, \n Please do not leave PlayCarry Boosting Services server to chat with this bot \n track orders and help with general issues. \n Please feel free to ask questions, we work around the clock and you will be answered within a few minutes!",
    color=0xffa500
  )
  # Добавление изображения
  embed.set_thumbnail(url="https://i.ytimg.com/vi/dxAmRhhQrGQ/maxresdefault.jpg")
  # Отправка в личное сообщение
  await member.create_dm()
  await member.dm_channel.send(embed=embed)

  # Создание нового контакта в Интеркоме
  headers = {
    "Authorization": f"Bearer {intercom_token}",
    "Accept": "application/json",
    "Content-Type": "application/json"
  }
  data = {
    "role":
    "user",
    "external_id":
    str(member.id),
    "name":
    str(member.name),
    "avatar":
    "https://cdn-icons-png.flaticon.com/512/4945/4945973.png"
  }
  
  
  response = requests.post("https://api.intercom.io/contacts",
                           json=data,
                           headers=headers)
  time.sleep(60)
  await member.dm_channel.send("** *Operator entered chat* **")
  # Поиск контакта в Интеркоме для получения его ID
  id_search = {
    "query": {
      "field": "external_id",
      "operator": "=",
      "value": str(member.id)
    }
  }
  id_search_response = requests.post("https://api.intercom.io/contacts/search",
                                     json=id_search,
                                     headers=headers)
  id_value = id_search_response.json()['data'][0]['id']
  
  # Создание диалога с контактом
  conversation_data = {
    "from": {
      "type": "user",
      "id": str(id_value)
    },
    "body": "Chat created from Discord"
  }
  conversation_response = requests.post(
    "https://api.intercom.io/conversations",
    json=conversation_data,
    headers=headers)

# Действия при новом сообщении
@client.event
async def on_message(message):
  if message.author.bot:
    return

  # Поиск контакта
  headers = {
    "Authorization": f"Bearer {intercom_token}",
    "Accept": "application/json",
    "Content-Type": "application/json"
  }

  id_search = {
    "query": {
      "field": "external_id",
      "operator": "=",
      "value": str(message.author.id)
    }
  }
  id_search_response = requests.post("https://api.intercom.io/contacts/search",
                                     json=id_search,
                                     headers=headers)

  id_value = id_search_response.json()['data'][0]['id']
  
# Поиск диалога
  id_conv_search = {
    "query": {
      "field": "contact_ids",
      "operator": "=",
      "value": id_value
    }
  }

  id_conv_response = requests.post("https://api.intercom.io/conversations/search",json=id_conv_search, headers=headers)
  id_conv_value = id_conv_response.json()['conversations'][0]['id']

# Пересылка сообщения в диалог
  
  conversation_data = {
    "message_type": "comment",
    "type": "user",
    "intercom_user_id": str(id_value),
    "body": message.content
  }
  conversation_response = requests.post(
    f"https://api.intercom.io/conversations/{id_conv_value}/reply",
    json=conversation_data,
    headers=headers)


client.run("MTA2MDczNTE1NjExNTIxODUyMw.G2EuhE.7uQvSaO5xwupb5ZDfGNU5zhW_GKa9wlKRFj7qI")