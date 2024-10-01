# reversi/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .game import ReversiGame


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'reversi_game'

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        self.game = ReversiGame()
        await self.send(json.dumps({'board': self.game.board}))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        row, col = data['row'], data['col']

        # Make the move
        self.game.make_move(row, col)

        # Broadcast the updated board to all players
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_board',
                'board': self.game.board,
                'current_player': self.game.current_player,
            }
        )

    async def send_board(self, event):
        board = event['board']
        current_player = event['current_player']

        await self.send(json.dumps({'board': board, 'current_player': current_player}))
