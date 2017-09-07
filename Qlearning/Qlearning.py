#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#宝探し (Q学習)
#Auther phuzeron

import random
import sys
import math

#状態
START = 0 #入口 (スタート)
WOOD = 1 #森
LAKE = 2 #湖
POND = 3 #池
FIELD = 4 #草原
GOAL = 5 #宝 (ゴール)

TrialNo = 50 #試行回数
StateNum = 6 #状態数
ActNum = 4 #行動数

Alpha = 0.1 #学習率
Gamma = 0.9 #減衰率

Reward = 10 #報酬


#乱数の発生 (0〜1の乱数)
def Random():
	return random.random()


#行動の選択 (ボルツマン選択)
#state : 状態
#Qvalue[s][a] : 状態sにおいて行動aを取ることの価値
#env[s][a] : 状態sにおいて行動aを取ったときに遷移する状態
#t : 試行回数
def select_action(state, Qvalue, env, t):
	sum_value = 0 #ルールの価値の合計
	border = 0 #境界線
	T = 10 #温度パラメータ

	#温度パラメータを設定
	T = T - t
	if T<=1 : T=1

	#ルールの価値の合計を計算 その状態で取れない行動(env[state][a]=-1) の価値は合計には含まない
	for a, value in enumerate(range(ActNum)):
		if env[state][a] != -1: sum_value += math.exp(Qvalue[state][a]/T)

	#0～sumの乱数を生成
	r = Random()*sum_value
	border = 0
	for a, actnum_value in enumerate(range(ActNum)):
		#取ることのできる行動の中から行動を選択
		if env[state][a] != -1: border += math.exp(Qvalue[state][a]/T)

		#選択された行動を返す
		if r <= border: return a


#ルールの価値の更新
#Qvalue[s][a] : 状態sにおいて行動aを取ることの価値
#p_state : 直前の状態
#act : 行動
#state : 状態 (行動後の状態)
#r : 報酬
def update_Q(Qvalue, p_state, act, state, r):
	max_value = 0 #行動後の状態から取ることのできる行動の中での価値の最大値

	#取ることのできる行動に関する価値の中で最大値を求める
	for index_j, value_j in enumerate(Qvalue[state]):
		max_value = max(Qvalue[state][index_j], max_value)

	#状態p_stateにおいて行動actをとることの価値を更新
	Qvalue[p_state][act] += Alpha * (r + Gamma * max_value - Qvalue[p_state][act])


#メインプログラム
t = 0 #試行回数
act = 0 #行動
p_state = 0 #直前の状態
state = 0 #状態
Qvalue = [[0 for i in range(ActNum)] for j in range(StateNum)] #ルールの価値 ルールの価値の初期化 Qvalue[s][a] : 状態sにおいて行動aを取ることの価値

#行動可能な方角とその先のノードを定義 方角は [東, 西, 南, 北] の順に定義
env = [[WOOD, -1, POND, -1], #入口
	 [LAKE, START, FIELD, -1], #森
	 [-1, WOOD, GOAL, -1], #湖
	 [FIELD, -1, -1, START], #池
	 [-1, POND, -1, WOOD]]; #草原

count = 0 #エピソードの長さ
states = ["入口","森","湖","池","草原","宝"] #状態(表示用)
acts = ["東","西","南","北"] #行動(表示用)

#結果保存用のファイル(result.dat)をオープン
result = None
try:
	result = open("result.dat", "w", encoding="utf-8-sig")
except Exception as e:
	print("Cannot open result.dat")
	sys.exit(1)


#TrialNo回の試行を繰り返す
for t, value in enumerate(range(TrialNo)):
	print(str(t)) #試行回数を出力
	state = START #状態を初期化(STARTに設定)
	count = 0 #エピソードの長さを0で初期化

	#ゴールに到達するまで繰り返す
	while state != GOAL:
		act = select_action(state,Qvalue,env,t) #行動を選択
		p_state = state #状態を保存
		state = env[p_state][act] #行動することにより状態が遷移

		#ゴールに到達したら報酬を取得し、ルールの価値を更新
		if state == GOAL:
			 update_Q(Qvalue, p_state, act, state, Reward)
		else:
			update_Q(Qvalue, p_state, act, state, 0)

		#状態と行動を画面に表示
		print(states[p_state] + "==>(" + acts[act] + ")==>", end="")
		#エピソードの長さを1増やす
		count += 1

	#最終的な状態を画面に表示
	print(states[state])
	#試行回数とエピソードの長さをファイルに出力
	result.write(str(t)+" "+str(count)+"\n")

#結果保存用のファイル(result.dat)を閉じる
result.close()

#最終的なルールの価値保存用のファイルをオープン
q = None
try:
	q = open("Q.dat", "w", encoding="utf-8-sig")
except Exception as e:
	print("Cannot open result.dat")
	sys.exit(1)

#ルールの価値をファイルに書き出す
q.write("　　　　　東　　　西　　　南　　　北\n")
for s, state_value in enumerate(range(StateNum)):
	q.write(str(states[s]) + "\t")
	for a, act_value in enumerate(range(ActNum)):
		q.write(str("%6.3f\t"%Qvalue[s][a]))

	q.write("\n")

#ファイルをクローズ
q.close()