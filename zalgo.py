import discord
import asyncio
import random
from sys import argv

chars = [

  ## super ##
	"\u030d", "\u030e", "\u0304", "\u0305", "\u033f",
	"\u0311", "\u0306", "\u0310", "\u0352", "\u0357",
	"\u0351", "\u0307", "\u0308", "\u030a", "\u0342",
	"\u0343", "\u0344", "\u034a", "\u034b", "\u034c",
	"\u0303", "\u0302", "\u030c", "\u0350", "\u0300",
	"\u030b", "\u030f", "\u0312", "\u0313", "\u0314",
	"\u033d", "\u0309", "\u0363", "\u0364", "\u0365",
	"\u0366", "\u0367", "\u0368", "\u0369", "\u036a",
	"\u036b", "\u036c", "\u036d", "\u036e", "\u036f",
	"\u033e", "\u035b", "\u0346", "\u031a"

  ## middle ##
	"\u0315", "\u031b", "\u0340", "\u0341", "\u0358",
	"\u0321", "\u0322", "\u0327", "\u0328", "\u0334",
	"\u0335", "\u0336", "\u034f", "\u035c", "\u035d",
	"\u035e", "\u035f", "\u0360", "\u0362", "\u0338",
	"\u0337", "\u0361", "\u0489"

  ## sub ##
	"\u0316", "\u0317", "\u0318", "\u0319", "\u031c",
	"\u031d", "\u031e", "\u031f", "\u0320", "\u0324",
	"\u0325", "\u0326", "\u0329", "\u032a", "\u032b",
	"\u032c", "\u032d", "\u032e", "\u032f", "\u0330",
	"\u0331", "\u0332", "\u0333", "\u0339", "\u033a",
	"\u033b", "\u033c", "\u0345", "\u0347", "\u0348",
	"\u0349", "\u034d", "\u034e", "\u0353", "\u0354",
	"\u0355", "\u0356", "\u0359", "\u035a", "\u0323"
]

client = discord.Client()

async def test(message):
  counter = 0
  tmp = await client.send_message(message.channel, 'Calculating messages...')
  async for log in client.logs_from(message.channel, limit=100):
      if log.author == message.author:
          counter += 1

  await client.edit_message(tmp, 'You have {} messages.'.format(counter))

async def zalgo_call(text):
  intensity = 2
  in_text = ''

  msg = text.content.split(' ')

  for arg in msg:
    if arg.startswith('-int='):
      try:
        intensity = int(arg[5:])
        if intensity > 200: ## catch if the intensity is TOO high
          intensity = 2
          await client.send_message(text.channel, '`INTENSITY OVERFLOW. RESTORING STATE TO 2`')
      except: ## catch if the user inputs an  e  v  i  l  string
        intensity = 2
        await client.send_message(text.channel, '`INTENSITY CORRUPTED BY  E V I L  STRING`')
    elif not arg.startswith('.z'):
      in_text += arg

  try:
    out = zalgo(intensity,in_text)
    await client.send_message(text.channel, out)
  except:
    await client.send_message(text.channel, zalgo() + ' oh no. something went wrong :( try reducing the intensity')

async def orang(msg):
  await client.send_message(msg.channel, msg.author.mention + zalgo())


def zalgo(intensity=2,text='AAAAAAAAAAAAAAAAAAAAA'): ## zalgoifier method
  new_text = ''

  for c in text:
    for i in range(intensity):
      c = random.choice(chars) + c + random.choice(chars)
    new_text += c
  return new_text

command_map = {
  '.z ' : zalgo_call,
  'ORANG' : orang
}


@client.event ## print some stuff to console when the bot is activated
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='WITH THE HIVE MIND'))

@client.event
async def on_message(message): ## when a message arrives at the bot ##
  for k,v in command_map.items():
    if message.content.startswith(k):
      await v(message)

if len(argv) < 2:
  print('Please remember you need to enter a token for your bot as an argument.')
else:
  client.run(argv[1])
