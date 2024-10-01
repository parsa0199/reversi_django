# game/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ReversiConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'reversi_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'Welcome to the Reversi game!',
            'board': self.get_initial_board(),
            'turn': 'black'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        move = text_data_json['move']
        turn = text_data_json['turn']

        # Here, handle the game logic to update the board
        new_board, new_turn = self.make_move(move, turn)

        # Send the updated board to all players
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_message',
                'board': new_board,
                'turn': new_turn
            }
        )

    async def game_message(self, event):
        board = event['board']
        turn = event['turn']

        await self.send(text_data=json.dumps({
            'board': board,
            'turn': turn
        }))

    def get_initial_board(self):
        # Create a 8x8 board with starting pieces
        board = [['' for _ in range(8)] for _ in range(8)]
        board[3][3] = 'white'
        board[3][4] = 'black'
        board[4][3] = 'black'
        board[4][4] = 'white'
        return board

    def make_move(self, move, turn):
        # Update the board with the player's move
        # This is a simplified example; you should add logic for validating moves, flipping pieces, etc.
        x, y = move
        board = self.get_initial_board()  # In a real game, you would retrieve the current board state here
        if board[x][y] == '':
            board[x][y] = turn
            new_turn = 'white' if turn == 'black' else 'black'
            return board, new_turn
        return board, turn
