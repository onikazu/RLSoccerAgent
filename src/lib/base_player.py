"""
base_player.py
基礎的なサッカープレイヤーエージェント
"""

from socket import *
import threading
import sys
import os


class BasePlayer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.HOSTNAME = "localhost"
        self.PORT = 6000
        self.ADDRESS = gethostbyname(self.HOSTNAME)
        self.m_strPlayMode = ""
        self.m_iNumber = 0
        self.m_strTeamName = ""
        self.m_strHostName = ""
        self.m_strSide = ""
        self.m_dKickOffX = 0.0
        self.m_dKickOffY = 0.0
        self.m_debugLv02 = False
        self.m_didPosition = False
        self.m_didTurn = False
        self.m_strFlagName = []
        self.m_dFlagX = []
        self.m_dFlagY = []
        self.m_debugLv08 = False
        self.m_dX = 0.0
        self.m_dY = 0.0
        self.m_dNeck = 0.0
        self.m_strFlagName.append("g r");
        self.m_dFlagX.append(52.5);
        self.m_dFlagY.append(0.0)
        self.m_strFlagName.append("g l");
        self.m_dFlagX.append(-52.5);
        self.m_dFlagY.append(0.0)
        self.m_strFlagName.append("f c t");
        self.m_dFlagX.append(0.0);
        self.m_dFlagY.append(-34.0)
        self.m_strFlagName.append("f c b");
        self.m_dFlagX.append(0.0);
        self.m_dFlagY.append(+34.0)
        self.m_strFlagName.append("f c");
        self.m_dFlagX.append(0.0);
        self.m_dFlagY.append(0.0)
        self.m_strFlagName.append("f p l t");
        self.m_dFlagX.append(-36.0);
        self.m_dFlagY.append(-20.16)
        self.m_strFlagName.append("f p l b");
        self.m_dFlagX.append(-36.0);
        self.m_dFlagY.append(20.16)
        self.m_strFlagName.append("f p l c");
        self.m_dFlagX.append(-36.0);
        self.m_dFlagY.append(0.0)
        self.m_strFlagName.append("f p r t");
        self.m_dFlagX.append(36.0);
        self.m_dFlagY.append(-20.16)
        self.m_strFlagName.append("f p r b");
        self.m_dFlagX.append(36.0);
        self.m_dFlagY.append(20.16)
        self.m_strFlagName.append("f p r c");
        self.m_dFlagX.append(36.0);
        self.m_dFlagY.append(0.0)
        self.m_strFlagName.append("f g l t");
        self.m_dFlagX.append(-52.5);
        self.m_dFlagY.append(-7.01)
        self.m_strFlagName.append("f g l b");
        self.m_dFlagX.append(-52.5);
        self.m_dFlagY.append(7.01)
        self.m_strFlagName.append("f g r t");
        self.m_dFlagX.append(52.5);
        self.m_dFlagY.append(-7.01)
        self.m_strFlagName.append("f g r b");
        self.m_dFlagX.append(52.5);
        self.m_dFlagY.append(7.01)
        self.m_strFlagName.append("f t l 50");
        self.m_dFlagX.append(-50.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t l 40");
        self.m_dFlagX.append(-40.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t l 30");
        self.m_dFlagX.append(-30.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t l 20");
        self.m_dFlagX.append(-20.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t l 10");
        self.m_dFlagX.append(-10.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t 0");
        self.m_dFlagX.append(0.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t r 10");
        self.m_dFlagX.append(10.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t r 20");
        self.m_dFlagX.append(20.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t r 30");
        self.m_dFlagX.append(30.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t r 40");
        self.m_dFlagX.append(40.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f t r 50");
        self.m_dFlagX.append(50.0);
        self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("f b l 50");
        self.m_dFlagX.append(-50.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b l 40");
        self.m_dFlagX.append(-40.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b l 30");
        self.m_dFlagX.append(-30.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b l 20");
        self.m_dFlagX.append(-20.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b l 10");
        self.m_dFlagX.append(-10.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b 0");
        self.m_dFlagX.append(0.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b r 10");
        self.m_dFlagX.append(10.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b r 20");
        self.m_dFlagX.append(20.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b r 30");
        self.m_dFlagX.append(30.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b r 40");
        self.m_dFlagX.append(40.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f b r 50");
        self.m_dFlagX.append(50.0);
        self.m_dFlagY.append(39.0)
        self.m_strFlagName.append("f l t 30");
        self.m_dFlagX.append(-57.5);
        self.m_dFlagY.append(-30.0)
        self.m_strFlagName.append("f l t 20");
        self.m_dFlagX.append(-57.5);
        self.m_dFlagY.append(-20.0)
        self.m_strFlagName.append("f l t 10");
        self.m_dFlagX.append(-57.5);
        self.m_dFlagY.append(-10.0)
        self.m_strFlagName.append("f l 0");
        self.m_dFlagX.append(-57.5);
        self.m_dFlagY.append(0.0)
        self.m_strFlagName.append("f l b 10");
        self.m_dFlagX.append(-57.5);
        self.m_dFlagY.append(10.0)
        self.m_strFlagName.append("f l b 20");
        self.m_dFlagX.append(-57.5);
        self.m_dFlagY.append(20.0)
        self.m_strFlagName.append("f l b 30");
        self.m_dFlagX.append(-57.5);
        self.m_dFlagY.append(30.0)
        self.m_strFlagName.append("f r t 30");
        self.m_dFlagX.append(57.5);
        self.m_dFlagY.append(-30.0)
        self.m_strFlagName.append("f r t 20");
        self.m_dFlagX.append(57.5);
        self.m_dFlagY.append(-20.0)
        self.m_strFlagName.append("f r t 10");
        self.m_dFlagX.append(57.5);
        self.m_dFlagY.append(-10.0)
        self.m_strFlagName.append("f r 0");
        self.m_dFlagX.append(57.5);
        self.m_dFlagY.append(0.0)
        self.m_strFlagName.append("f r b 10");
        self.m_dFlagX.append(57.5);
        self.m_dFlagY.append(10.0)
        self.m_strFlagName.append("f r b 20");
        self.m_dFlagX.append(57.5);
        self.m_dFlagY.append(20.0)
        self.m_strFlagName.append("f r b 30");
        self.m_dFlagX.append(57.5);
        self.m_dFlagY.append(30.0)
        self.m_strFlagName.append("f l t");
        self.m_dFlagX.append(-52.5);
        self.m_dFlagY.append(-34.0)
        self.m_strFlagName.append("f l b");
        self.m_dFlagX.append(-52.5);
        self.m_dFlagY.append(34.0)
        self.m_strFlagName.append("f r t");
        self.m_dFlagX.append(52.5);
        self.m_dFlagY.append(-34.0)
        self.m_strFlagName.append("f r b");
        self.m_dFlagX.append(52.5);
        self.m_dFlagY.append(34.0)

        self.m_dBallX = 0.0
        self.m_dBallY = 0.0
        self.m_dDefenceX = 0.0
        self.m_dDefenceY = 0.0

        self.OUT_OF_RANGE = 999.9
        self.m_iTime = 0
        self.m_strCommand = ""
        self.m_dStamina = 8000
        self.m_strPlayerType = []
        for _ in range(20):
            self.m_strPlayerType.append("")

    # コマンドの送信
    def send(self, command):
        if len(command) == 0:
            return
        command = command + "\0"
        try:
            to_byte_command = command.encode(encoding='utf_8')
            self.socket.sendto(to_byte_command, (self.ADDRESS, self.PORT))
        except OSError:
            print("送信失敗")
            sys.exit()

    # メッセージの受信
    def receive(self):
        try:
            message, arr = self.socket.recvfrom(4096)
            message = message.decode("UTF-8")
            self.PORT = arr[1]
            return message
        except OSError:
            print("受信失敗")
            sys.exit()

    def initialize(self, number, team_name, server_name, server_port):
        self.m_iNumber = number
        self.m_strTeamName = team_name
        self.m_strHostName = server_name
        self.PORT = server_port
        if self.m_iNumber == 1:
            command = "(init " + self.m_strTeamName + "(goalie)(version 15.40))"
        else:
            command = "(init " + self.m_strTeamName + "(version 15.40))"
        self.send(command)
        
        # ログ・ファイルの初期化確認
        if not os.path.isfile("../logs/{0}_{1}_reward.log".format(self.m_strTeamName, self.m_iNumber)):
            with open("../logs/{0}_{1}_reward.log".format(self.m_strTeamName, self.m_iNumber), "w") as the_file:
                the_file.write("")
        if not os.path.isfile("./logs/{0}_{1}_command.log".format(self.m_strTeamName, self.m_iNumber)):
            with open("../logs/{0}_{1}_command.log".format(self.m_strTeamName, self.m_iNumber), "w") as the_file:
                the_file.write("")
        else:
            pass

    # thread を動かしている最中に行われる関数
    def run(self):
        while True:
            message = self.receive()
            # print(message)
            self.analyzeMessage(message)
                      
    def analyzeMessage(self, message):
        return 


if __name__ == "__main__":
    players = []
    for i in range(11):
        p = BasePlayer()
        players.append(p)
        players[i].initialize(i+1, "kazu", "localhost", 6000)
        players[i].start()
    print("試合登録完了")
