# Chatty.py

Chatty.py is a library made in Python for making Chatty bots.

# Example
For a simple example, see [example.py](src/chatty.py/example.py).
An even simpler example is shown bellow:

```python
from chattypy import bot

bot = bot.Client(name='Example Bot', channel='hangout')

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
    bot.send_msg(f'Help requested by @{cmd.author.name}')

bot.run()
```