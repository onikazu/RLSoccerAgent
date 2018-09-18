"""
train.py
強化学習クライアントを訓練させる
"""

import subprocess
import os
import time


# エピソード数
episodes = 1000
# ステップ数
step = 1000
# 実行ファイル名
exe_program = "dqn_player.py"


if __name__ == "__main__":
    # 本番学習スタート
    print("start")
    for episode in range(episodes):
        # ディレクトリの移動
        os.chdir("../")
        os.chdir("../")

        # サーバの起動
        cmd = \
            "rcssserver server::send_step = 3 server::sense_body_step = 2 server::simulator_step = 2 server::auto_mode = true server::connect_wait = 800"
        server = subprocess.Popen(cmd.split())

        # モニタの起動
        cmd = "soccerwindow2"
        window = subprocess.Popen(cmd.split())

        # ディレクトリの移動
        os.chdir("./RLSoccerAgent/src")

        # モデル・ログフォルダがなければ作成
        if not os.path.isdir("./models"):
            os.mkdir("./models")

        if not os.path.isdir("./logs"):
            os.mkdir("./logs")

        if not os.path.isdir("./memorys"):
            os.mkdir("./memorys")

        # クライアントプログラムの実行
        cmd = "python3 {} {} {}".format(exe_program, episode, step)
        client = subprocess.Popen(cmd.split())

        # 学習
        # while True:
        #     if zidan2.episode_finish_flag is True:
        #         break
        time.sleep(15)
        print("episode{} is done ".format(episode))

        # サーバの削除
        server.kill()
        # ウィンドウの削除
        window.kill()
        # クライアントの削除
        client.kill()

    print("end")
