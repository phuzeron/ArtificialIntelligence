#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#狼と山羊とキャベツと男の問題 (深さ優先探索)
#Auther phuzeron

import copy
import sys

MAN = 0
WOLF = 1
GOAT = 2
CABBAGE = 3

SearchMax = 20

left_side = [[0 for j in range(4)] for i in range(SearchMax)] #左岸の状態
right_side = [[0 for j in range(4)] for i in range(SearchMax)] #右岸の状態


#状態の表示
#引数 state[i] : 左岸もしくは右岸の状態
#state[i]の配列の内容に応じて状態を表示する
#(例) state[i]={1,1,1,1}ならば [ 男 狼 山羊 キャベツ ]
#       state[i]={1,0,1,0}ならば [ 男 山羊 ]
#       state[i]={0,0,0,0}ならば [  ]
def print_state(state):
	print_buffer = "[ "
	for index, value in enumerate(state):
		if index == MAN and value == 1 : print_buffer += "男 "
		if index == WOLF and value == 1 : print_buffer += "狼 "
		if index == GOAT and value == 1 : print_buffer += "山羊 "
		if index == CABBAGE and value == 1 : print_buffer += "キャベツ "
	print_buffer += "]"
	print(print_buffer, end='')


#結果の表示 
#引数 T : ステップ数
#Tステップ目までの結果を表示する
#ステップ数: [ 左岸の状態 ] [ 右岸の状態 ]  
#(例) 0: [ 男 狼 山羊 キャベツ ] [ ] 
#       1: [ 狼 山羊 ] [ 男 キャベツ ] 
def print_ans(T):
	for t, value in enumerate(range(T+1)):
		print(str(t) + ": ", end='')
		print_state(left_side[t])
		print_state(right_side[t])
		print("")


#状態のチェック
#引数 T : ステップ数
#       state[i] : チェックしたい状態
#       past_state[t][i] : 過去の状態(tステップ目の状態)
#・狼と山羊、山羊とキャベツを残した状態でもなく、既に探索された状態でもなければTrueを返す
#・それ以外はFalseを返す
def check_state(T, state, past_state):
	#狼と山羊 もしくは 山羊とキャベツが一緒にないかをチェックあればFalseを返す
	if (state[1]==1 and state[2]==1) or (state[2]==1 and state[3]==1): return False

	#過去に同じ状態がないかをチェック  あればFalseを返す
	for t, value in enumerate(range(T)):
		for i, j in enumerate(range(4)):
			if past_state[t][0]==state[0] and past_state[t][1]==state[1] and past_state[t][2]==state[2] and past_state[t][3]==state[3]: return False

	return True


#深さ優先探索
#引数 T : ステップ数
#       src_side[t][i] : 男がいる側の状態
#       dest_side[t][i] : 男がいない側の状態
def search(T, src_side, dest_side):
	src_state =[0]*4 #男がいる側の状態
	dest_state =[0]*4 #男がいない側の状態
	new_src_state =[0]*4 #男がいる側の次のステップの状態
	new_dest_state =[0]*4 #男がいない側の次のステップでの状態

	#Tステップ目の状態をコピー
	for i, value in enumerate(range(4)):
		src_state[i] = src_side[T][i]
		dest_state[i] = dest_side[T][i]

	#0: 男 1: 狼 2: 山羊 3: キャベツ を順に調べる
	for i, value in enumerate(range(4)):
		#移動できるのであれば(男と同じ側にいるのであれば)iと男を移動(iが0の場合は男のみ移動)した後の状態をnew_src_state[], new_dest_state[] に格納 
		if src_state[i]==1:
			new_src_state = copy.deepcopy(src_state)
			new_dest_state = copy.deepcopy(dest_state)
			new_src_state[0] = 0
			new_dest_state[0] = 1
			new_src_state[i] = 0
			new_dest_state[i] = 1

			# iと男を移動(iが0の場合は男のみ移動)した後の状態が有効かどうかを チェックし、有効であれば 岸の状態を更新し、次に進む
			if check_state(T, new_src_state, src_side):
				#男が左岸にいる場合(Tが偶数の場合)
				if T%2 == 0:
					 left_side[T+1] = copy.deepcopy(new_src_state)
					 right_side[T+1] = copy.deepcopy(new_dest_state)
				else: #男が右岸にいる場合(Tが奇数の場合)
					right_side[T+1] = copy.deepcopy(new_src_state)
					left_side[T+1] = copy.deepcopy(new_dest_state)

				#右岸にすべてが移動していれば 結果を表示して終了
				for index_i, value_i in enumerate(right_side):
					for index_j, value_j in enumerate(right_side[index_i]):
						if value_j != 0:
							print_ans(T+1)
							sys.exit()
						else: #そうでなければ再帰的に探索を続ける
							search(T+1, dest_side, src_side)


#メインプログラム
#配列の初期化 (-1を設定)
for t, value_i in enumerate(range(SearchMax)):
	for i, value_j in enumerate(range(4)):
		left_side[t][i] = -1
		right_side[t][i] = -1

#初期状態の設定
for i, value_j in enumerate(range(4)):
	left_side[0][i]=1;
	right_side[0][i]=0;

#探索
search(0, left_side, right_side)
