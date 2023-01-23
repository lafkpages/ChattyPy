import websocket #upm package(websocket-client)
import json

class Client(object):
  def __init__(self, server = 'chatty.ktat.repl.co', channel = None, name = None, info = 'Bot info', image = '/avatars/helper.svg'):
    self.server = server
    self.channel = channel

    self.name = name
    self.info = info
    self.image = image

    self.token = None

    self.ws = None

    # User registered event handlers
    self._on_ready_handlers = []
    self._on_message_handlers = []
    self._on_slash_handlers = []

  def _on_open(self, ws):
    for handler in self._on_ready_handlers:
      handler()

  def _on_message(self, ws, data):
    data = json.loads(data)

    if 'token' in data and not self.token:
      self.token = data['token']

      self.ws.send(json.dumps({
        'type': 'bot',
        'bot': {
          'name': self.name,
          'info': self.info,
          'image': self.image
        },
        'wssMessageData': {
          'token': self.token,
          # 'slashId': ''
        }
      }))
    elif 'type' in data:
      t = data['type']

      if t == 'message':
        # Create a message class
        msg = Message(data, self)

        # Call handlers
        for handler in self._on_message_handlers:
          handler(msg)
      elif t == 'slash':
        # Create a slash command class
        cmd = SlashCommand(data, self)

        # Call handlers
        for handler in self._on_slash_handlers:
          handler(cmd)
      else:
        print('Unknown WebSocket message:', data)

  def _on_error(self, ws, error):
    raise error

  def on_ready(self, func):
    self._on_ready_handlers.append(func)
    return func

  def on_message(self, func):
    self._on_message_handlers.append(func)
    return func

  def on_command(self, func):
    self._on_slash_handlers.append(func)
    return func

  def run(self):
    if not self.name:
      raise TypeError('no bot name specified')

    if not self.channel:
      raise TypeError('no channel specified')

    wssUrl = f'wss://{self.server}/b/{self.channel}'
    self.ws = websocket.WebSocketApp(wssUrl, on_open=self._on_open, on_message=self._on_message, on_error=self._on_error)
    self.ws.run_forever()

  def send_msg(self, msg):
    if not self.ws:
      raise RuntimeError('tried to send message without connecting to server')

    self.ws.send(json.dumps({
      'type': 'sendMessage',
      'data': msg,
      'wssMessageData': {
        'token': self.token
      }
    }))


class Message(object):
  def __init__(self, data, bot):
    self.author = User(data['who'])
    self.text_content = data.get('srcMessage')
    self.html_content = data.get('message')

    self.bot = bot

  def __str__(self):
    return self.text_content


class SlashCommand(Message):
  def __init__(self, data, bot):
    super().__init__(data, bot)

    self.args = data['command']
    self.cmd = self.args.pop(0)
    self.args_str = ' '.join(self.args)
    self.id = data['id']

  def __str__(self):
    return self.cmd

  def __repr__(self):
    return f'/{self.bot.name} {self.args_str}'


class User(object):
  def __init__(self, data):
    self.name = data['name']
    self.id = data['id']
    self.profile_image = data['profileImage']

    self.is_typing = data.get('isTyping')

  def __repr__(self):
    return f'{self.name} ({self.id})'