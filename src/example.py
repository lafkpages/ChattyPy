from chattypy import bot

bot = bot.Client(name='ChattyPy', channel='hangout')

@bot.on_ready
def on_ready():
  print('Bot ready!')

@bot.on_message
def on_message(msg):
  print('User', msg.author, 'sent message:', msg)

@bot.on_command
def on_command(cmd):
  print('User', cmd.author, 'sent slash command:', cmd)

  if cmd.cmd == 'help':
    bot.send_msg(f'Help requested by @{cmd.author.name}\n\nChattyPy is a library made in Python for making Chatty bots.\n\nFor more info, see [the GitHub repo](https://github.com/lafkpages/Chatty.py).')
  elif cmd.cmd == 'add':
    bot.send_msg(f'{cmd.args[0]} + {cmd.args[1]} = {float(cmd.args[0]) + float(cmd.args[1])}')
  elif cmd.cmd == 'whoami':
    bot.send_msg(f'You are [`@{cmd.author.name}` on Replit](https://id.raadsel.repl.co/api/u/{cmd.author.id})\n![profile image]({cmd.author.profile_image})')

bot.run()