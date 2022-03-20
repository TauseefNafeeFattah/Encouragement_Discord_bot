import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()
sad_word_list = ["sad","depressed","unhappy","miserable","angry","depressing"]
starter_encouragements_list = ["Cheer Up!","Hang in there","You have got this"]
db["respond_status"] = False;
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

def update_encouragements(encouragement_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouragement_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"]=[encouragement_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements)> index:
    del encouragements[index]
    db["encouragements"] = encouragements

def update_responding(status):
  db["respond_status"] = status
  
@client.event
async def on_ready():
  print("we have logged in as{0.user}".format(client))

@client.event

async def on_message(message):
  
  if message.author==client.user:
    return
  
  if message.content.startswith('$hello'):
	  await message.channel.send('Hello!')
  elif message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  elif any(word in message.content for word in sad_word_list) and db["respond_status"]:
    options = starter_encouragements_list
    if "encouragements" in db.keys():
      options.extend( db["encouragements"])
    await message.channel.send(random.choice(options))
    
      
  elif message.content.startswith("$new"):
    encouraging_message = message.content.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added")
  
  elif message.content.startswith('$del'):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
      index = int(message.content.split("$del ",1)[1])
      delete_encouragement(index)
      encouragements.extend( db["encouragements"])
    await message.channel.send(encouragements)
  
  elif message.content.startswith('$responding'):
    responding_status = message.content.split("$responding ",1)[1]
    if responding_status=="True":
      db["respond_status"] = True;
      await message.channel.send("responding to sad words is now turned on")
    else:
      db["respond_status"] = False;
      await message.channel.send("responding to sad words is now turned off")
  
    

my_secret = os.environ['TOKEN']
keep_alive()
client.run(my_secret)

