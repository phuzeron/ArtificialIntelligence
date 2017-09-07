#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#遺伝的アルゴリズム
#Auther phuzeron

import os
import random
import copy

POP_SIZE = 5 #個体数 (必ず奇数に設定)
G_LENGTH = 10 #個体の遺伝子型のビット数
MAX_GEN = 20 #世代数
M_RATE = 0.1 #突然変異率 (0〜1)


#乱数の発生 (0〜1の乱数)
def Random():
	return random.random()


#遺伝子の初期化
#引数 gene[p][i] : 遺伝子pのi番目の成分
def  init_gene(gene):
	#遺伝子を初期化  0〜1の乱数を発生し、0.5以上なら1 0.5未満なら0
	print("\n<< 初期個体群 >>")
	for i, p in enumerate(gene):
		for j, q in enumerate(gene[i]):
			if Random() < 0.5:
				gene[i][j] = 0
			else:
				gene[i][j] = 1


#適応度の計算
#引数 gene[p][i] : 遺伝子pのi番目の成分
#       fitness[p] : 遺伝子pの適応度
def calc_fitness(gene, fitness):
	#適応度の計算 前半の5bitは0の数 後半の5bitは1の数
	for i, p in enumerate(gene):
		fitness[i] = 0 #前世代の適応度をリセット
		first_slice = p[:5] #前半の5ビット
		latter_slice = p[5:] #後半の5ビット

		#前半の遺伝子の成分が0だったら適応度を1増やす
		for fs in first_slice:
			if fs == 0: fitness[i] += 1

		#後半の遺伝子の成分が1だったら適応度を1増やす
		for ls in latter_slice:
			if ls == 1: fitness[i] += 1


#遺伝子の表示 & 最大適応度・平均適応度の計算 & ファイルへの書き出し
#引数 t : 世代数
#       gene[p][i] : 遺伝子pのi番目の成分
#       fitness[p] : 遺伝子pの適応度
#       fp : ファイルポインタ
def show_gene(t, gene, fitness, fp):
	avg_fit = 0.0 #平均適応度
	max_fit = 0.0 #最大適応度

	#個体の値、適応度の表示
	for i, p in enumerate(gene):
		print("個体 " + str(p) , end="")
		print("  適応度 " + str(fitness[i]))

	#平均適応度の計算
	avg_fit = sum(fitness)/len(fitness)

	#最大適応度の計算
	max_fit = max(fitness)

	#平均・最大適応度の表示
	print("平均適応度 : " + str(avg_fit))
	print("最大適応度 : " + str(max_fit))

	#ファイルへの書き出し
	fp.write(str(t)+" "+str(avg_fit)+" "+str(max_fit) + "\n")


#個体番号 p1 と p2 の適応度と遺伝子を交換
#引数 p1, p2 : 遺伝子の番号
#       gene[p][i] : 遺伝子pのi番目の成分
#       fitness[p] : 遺伝子pの適応度
def swap_gene(p1, p2, gene, fitness):
	#遺伝子型の交換 (遺伝子p1と遺伝子p2の値を入れ替える)
	gene[p1], gene[p2] = gene[p2], gene[p1]

	#適応度の交換 (遺伝子p1と遺伝子p2の適応度の値を入れ替える)
	fitness[p1], fitness[p2] = fitness[p2], fitness[p1]


#個体番号 p1 の適応度と遺伝子型を p2 にコピー
#引数 p1, p2 : 遺伝子の番号
#       gene[p][i] : 遺伝子pのi番目の成分
#       fitness[p] : 遺伝子pの適応度
def copy_gene(p1, p2, gene, fitness):
	#遺伝子のコピー (遺伝子p1を遺伝子p2にコピーする)
	gene[p2] = copy.deepcopy(gene[p1])

	#適応度のコピー (遺伝子p1の適応度を遺伝子p2の適応度にコピーする)
	fitness[p2] = copy.deepcopy(fitness[p1])


#エリート保存
#(最小適応度の個体に最大適応度の個体のデータをコピー)
#引数 gene[p][i] : 遺伝子pのi番目の成分
#       fitness[p] : 遺伝子pの適応度
def elite(gene, fitness):
	#最大適応度の個体(max_p)と最小適応度の個体(min_p)を見つける
	max_p = fitness.index(max(fitness))
	min_p = fitness.index(min(fitness))

	#最小適応度の個体に最大適応度の個体をコピー
	copy_gene(max_p, min_p, gene, fitness)
	#最大適応度の個体を0番目に移動
	swap_gene(0, max_p, gene, fitness);


#ルーレット選択
#引数 gene[p][i] : 遺伝子pのi番目の成分
#       fitness[p] : 遺伝子pの適応度
def reproduction(gene, fitness):
	sum_of_fitness = sum(fitness) #個体の適応度の総和 ルーレットの1周分 sum_of_fitness を求める
	new_gene = [[0 for i in range(G_LENGTH)] for j in range(POP_SIZE)] #新しい遺伝子

	#ルーレットを POP_SIZE 回だけ回して次世代の個体を選ぶ
	for p in range(1, POP_SIZE):
		#ルーレットを回して場所を選ぶ
		#r : 選ばれた位置 (0 <= r <= sum_of_fitness)
		r = sum_of_fitness * Random()

		#選ばれた場所に該当する個体が何番か調べる
		#num : 選ばれた個体の番号 (0 <= num <= POP_SIZE-1)
		num = 0
		border = fitness[0] #ルーレット上の個体間の境界
		while border < r :
			num += 1
			border += fitness[num]

		#遺伝子の代入
		for i in range(G_LENGTH):
			new_gene[p][i] = gene[num][i]

	#遺伝子のコピー
	for p in range(1, POP_SIZE):
		for i in range(G_LENGTH):
			gene[p][i] = new_gene[p][i]


#一点交叉
#引数 gene[p][i] : 遺伝子pのi番目の成分
def crossover(gene):
	c_pos = random.randint(1, G_LENGTH-1) #交叉位置 (1 <= c_pos <= G_LENGTH-1)

	#交叉位置を1〜G_LENGTH-1の範囲でランダムに決め、それより後ろを入れ替える。
	#gene[1]とgene[2],  gene[3]とgene[4] ... のように親にする
	for i, g in enumerate(gene):
		if i % 2 == 1: #奇数番目の遺伝子
			for j in range(c_pos, len(gene[i])):
				try:
					gene[i][j], gene[i+1][j] = gene[i+1][j], gene[i][j]
				except IndexError:
					pass


#突然変異
#引数 gene[p][i] : 遺伝子pのi番目の成分
def mutation(gene):
	#0〜1の乱数を発生させ、その値が M_RATE 以下ならば、遺伝子の値をランダムに変える
	for g in gene[1:]:
		for i, v in enumerate(g):
			if Random() < M_RATE:
				g[i] = (not v) * 1


#メインプログラム
gene = [[0 for i in range(G_LENGTH)] for j in range(POP_SIZE)] #遺伝子
fitness = [0.0 for i in range(POP_SIZE)] #適応度

#適応度の変化を記録するファイルのオープン
try:
	fp = open("result.dat","w")
except Exception:
	print("Cannot open \"result.dat\"")
	os.exit(1)

#シミュレーション条件の表示
print("個体数 : " + str(POP_SIZE))
print("遺伝子長 : " + str(G_LENGTH))
print("突然変異率 : " + str(M_RATE))

init_gene(gene) #遺伝子の初期化
calc_fitness(gene, fitness) #適応度の計算
show_gene(0, gene, fitness, fp) #表示

for t in range(1, MAX_GEN +1):
	print("\n<< 世代数 : " + str(t) + " >>")
	elite(gene, fitness) #エリート保存
	reproduction(gene, fitness) #ルーレット選択
	crossover(gene) #単純交叉
	mutation(gene) #突然変異
	calc_fitness(gene, fitness) #適応度の計算
	show_gene(t, gene ,fitness, fp) #表示

#ファイルのクローズ
fp.close()
