"""
dqn_player.py
DQN で学習を行うサッカープレイヤーエージェント
"""

from lib import analyze_player
import threading


class DQNPlayer(analyze_player.AnalyzePlayer, threading.Thread):
    def __init__(self):
        super(DQNPlayer, self).__init__()

    # コマンド送信前に行う
    def beforeSendCommand(self):
        return








