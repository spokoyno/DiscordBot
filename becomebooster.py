import os, re, discord
from discord.ext import commands
import requests
import json

intercom_token = "dG9rOjgyNWRjZjg0XzFhZjVfNDI1M19iZDM3X2E4ZGM5NmI1MTYwYzoxOjA="

SERVER_ID = 972874770699915265 # Ввести ID сервера

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command(name="becomebooster")
async def assign_role(ctx, role_id: int):
    server = bot.get_guild(SERVER_ID)
    role = discord.utils.get(server.roles, id=role_id)
    member = await server.fetch_member(ctx.author.id)
    if role and member:
        try:
            await member.add_roles(role, reason="Assigned by bot command.")
        except discord.Forbidden:
            await ctx.send("Недостаточно прав.")
        except discord.HTTPException as e:
            await ctx.send(f"Ошибка: {e}")
        else:
            await ctx.send(f"Congratulations, you are now {role.name} in the PlayCarry company, {member.name} ! \nLog in to the server and check what's available to you :) ")
            
            
            
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
                  "value": str(ctx.author.id)
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
            
            headers = {
                "Authorization": f"Bearer {intercom_token}",
                "Accept": "application/json",
                "Content-Type": "application/json"
                      }
            data = {
  
                "type": "team",
                "admin_id": "5356360",
                "assignee_id": "5878150",
                "message_type": "assignment",
                "body": "Перешёл в команду бустеров",
                    }

            response = requests.post(f"https://api.intercom.io/conversations/{id_conv_value}/parts",
                           json=data,
                           headers=headers)
    else:
        await ctx.send("Role or user not found.")

      
bot.run("MTA2MDczNTE1NjExNTIxODUyMw.G2EuhE.7uQvSaO5xwupb5ZDfGNU5zhW_GKa9wlKRFj7qI")