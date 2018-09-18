"""
dqn_player.py
DQN で学習を行うサッカープレイヤーエージェント
"""

import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import load_model
from keras.utils import plot_model
from keras import backend as K
import tensorflow as tf
import pickle

from collections import deque
import time
import threading
import sys
import os

from lib import analyze_player, robo_tools


class DQNPlayer(analyze_player.AnalyzePlayer, threading.Thread):
    def __init__(self):
        super(DQNPlayer, self).__init__()
        self.num_episodes = 1000  # 総試行回数
        self.max_number_of_steps = 1000  # 1試行のstep数
        self.gamma = 0.99  # 割引係数
        self.islearned = 0  # 学習が終わったフラグ
        self.hidden_size = 16  # Q-networkの隠れ層のニューロンの数
        self.learning_rate = 0.00001  # Q-networkの学習係数
        self.memory_size = 10000  # バッファーメモリの大きさ
        self.batch_size = 32  # Q-networkを更新するバッチの大記載

        self.mainQN = QNetwork(hidden_size=self.hidden_size, learning_rate=self.learning_rate, m_strSide=self.m_strSide, m_iNumber=self.m_iNumber)  # メインのQネットワーク
        self.targetQN = QNetwork(hidden_size=self.hidden_size, learning_rate=self.learning_rate, m_strSide=self.m_strSide, m_iNumber=self.m_iNumber)  # 価値を計算するQネットワーク
        self.memory = Memory(max_size=self.memory_size, m_iNumber=self.m_iNumber, m_strSide=self.m_strSide)
        self.actor = Actor()

        self.state = [self.m_dX, self.m_dY, self.m_dBallX, self.m_dBallY, self.m_dStamina]
        self.actions = ("(turn 0)", "(turn 60)", "(turn -60)", "(dash 100)", "(kick 100 0)", "(kick 50 60)", "(kick 50 -60)")
        self.actions_select = 0
        self.reward = 0
        self.episode_reward = 0
        self.episode = int(sys.argv[2])
        self.step = 0

        self.targetQN = self.mainQN

    def beforeSendCommandFirstTime(self):
        if self.step == 0:
            return
        self.actions_select = self.actor.get_action(self.state, self.episode, self.mainQN)
        self.m_strCommand = self.actions[self.actions_select]

        self.step += 1


    def beforeSendCommand(self):
        if self.step > 0:
            return
        next_state = [self.m_dX, self.m_dY, self.m_dBallX, self.m_dBallY, self.m_dStamina]
        next_state = np.reshape(next_state, [1, len(next_state)])
        self.calc_reward()
        self.episode_reward += self.reward
        self.memory.add((self.state, self.actions_select, self.reward, next_state))  # メモリの更新する
        self.state = next_state  # 状態更新

        self.actions_select = self.actor.get_action(self.state, self.episode, self.mainQN)
        self.m_strCommand = self.actions[self.actions_select]
        print(self.m_strCommand)
        self.step += 1

    def calc_reward(self):
        self.reward = 0
        # 右チーム
        if self.m_strSide.startswith("r"):
            # ゴールすれば
            if self.m_strPlayMode == "(goal_r)":
                self.reward += 1000

        # 左チーム
        if self.m_strSide.startswith("l"):
            # ゴールすれば
            if self.m_strPlayMode == "(goal_l)":
                self.reward += 1000

        # 共通
        # ボールをキックできれば
        if robo_tools.getDistance(self.m_dX, self.m_dY, self.m_dBallX, self.m_dBallY) <= 0.7 and \
                self.m_strCommand.startswith("(kick"):
            self.reward += 1

    def checkFinishLearn(self):
        if self.step % self.max_number_of_steps == 0 and self.step != 0:
            print("{}episode finished".format(self.episode))
            # モデル・メモリの保存
            self.mainQN.model.save("./models/main_model{}{}.h5".format(self.m_strSide, self.m_iNumber))
            self.targetQN.model.save("./models/target_model{}{}.h5".format(self.m_strSide, self.m_iNumber))
            with open('./memorys/memory{}{}.pickle'.format(self.m_strSide, self.m_iNumber), mode='wb') as f:
                pickle.dump(self.memory, f)
            # 報酬ログの保存
            with open('./logs/reward{}{}'.format(self.m_strSide, self.m_iNumber), mode="a") as f:
                f.write("{0:d},{1:d}\n".format(self.episode, self.episode_reward))
            time.sleep(100)

# [1]損失関数の定義
# 損失関数にhuber関数を使用します 参考https://github.com/jaara/AI-blog/blob/master/CartPole-DQN.py
def huberloss(y_true, y_pred):
    err = y_true - y_pred
    cond = K.abs(err) < 1.0
    L2 = 0.5 * K.square(err)
    L1 = (K.abs(err) - 0.5)
    loss = tf.where(cond, L2, L1)  # Keras does not cover where function in tensorflow :-(
    return K.mean(loss)


class QNetwork:
    def __init__(self, learning_rate=0.01, state_size=5, action_size=7, hidden_size=10, m_strSide="right", m_iNumber=1):
        if os.path.isfile("./models/main_model{}{}.h5".format(m_strSide, m_iNumber)):
            self.model = load_model("./models/main_model{}{}.h5".format(m_strSide, m_iNumber))
        self.model = Sequential()
        self.model.add(Dense(hidden_size, activation='relu', input_dim=state_size))
        self.model.add(Dense(hidden_size, activation='relu'))
        self.model.add(Dense(action_size, activation='linear'))
        self.optimizer = Adam(lr=learning_rate)  # 誤差を減らす学習方法はAdam
        # self.model.compile(loss='mse', optimizer=self.optimizer)
        self.model.compile(loss=huberloss, optimizer=self.optimizer)

    # 重みの学習
    def replay(self, memory, batch_size, gamma, targetQN):
        inputs = np.zeros((batch_size, 5))
        targets = np.zeros((batch_size, 7))
        mini_batch = memory.sample(batch_size)

        for i, (state_b, action_b, reward_b, next_state_b) in enumerate(mini_batch):
            inputs[i:i + 1] = state_b
            target = reward_b

            if not (next_state_b == np.zeros(state_b.shape)).all(axis=1):
                # 価値計算（DDQNにも対応できるように、行動決定のQネットワークと価値観数のQネットワークは分離）
                retmainQs = self.model.predict(next_state_b)[0]
                next_action = np.argmax(retmainQs)  # 最大の報酬を返す行動を選択する
                target = reward_b + gamma * targetQN.model.predict(next_state_b)[0][next_action]

            targets[i] = self.model.predict(state_b)  # Qネットワークの出力
            targets[i][action_b] = target  # 教師信号
            self.model.fit(inputs, targets, epochs=1, verbose=0)  # epochsは訓練データの反復回数、verbose=0は表示なしの設定


# [3]Experience ReplayとFixed Target Q-Networkを実現するメモリクラス
class Memory:
    def __init__(self, max_size=1000, m_strSide="right", m_iNumber=1):
        if os.path.isfile("./memorys/memory{}{}.pickle".format(m_strSide, m_iNumber)):
            with open("./memorys/memory{}{}.pickle".format(m_strSide, m_iNumber), mode='rb') as f:
                self.buffer = pickle.load(f)
            return
        self.buffer = deque(maxlen=max_size)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self, batch_size):
        idx = np.random.choice(np.arange(len(self.buffer)), size=batch_size, replace=False)
        return [self.buffer[ii] for ii in idx]

    def len(self):
        return len(self.buffer)


# [4]カートの状態に応じて、行動を決定するクラス
class Actor:
    def get_action(self, state, episode, targetQN):  # [C]ｔ＋１での行動を返す
        # 徐々に最適行動のみをとる、ε-greedy法
        epsilon = 0.001 + 0.9 / (1.0 + episode)

        if epsilon <= np.random.uniform(0, 1):
            retTargetQs = targetQN.model.predict(state)[0]
            action = np.argmax(retTargetQs)  # 最大の報酬を返す行動を選択する

        else:
            action = np.random.choice([0, 1])  # ランダムに行動する

        return action

if __name__ == "__main__":
    plays = []
    for i in range(4):
        p = DQNPlayer()
        plays.append(p)
        teamname = str(p.__class__.__name__)
        if i < 11:
            teamname += "left"
        else:
            teamname += "right"
        plays[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        plays[i].start()
