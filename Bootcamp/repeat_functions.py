"""
Those funcions might have power to send messages
"""
from local_info import USERS

async def is_desired_game_on_sale(message, games):
    sale_desired_games = []

    for game in games:
        for desired_user_game in USERS[message.from_user.id]:
            if game['link'] == desired_user_game+"/?snr=1_7_7_2300_150_1":
                sale_desired_games.append(game)
                
    return sale_desired_games

