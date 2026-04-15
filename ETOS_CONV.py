# logging　config
from logging import getLogger, config
import json
with open('./log_config.json', 'r') as f:
    log_conf = json.load(f)
config.dictConfig(log_conf) #ロギング設定を取得
logger = getLogger(__name__)  #アプリ名でロギング
# logging　config END

import sys
import re
import itertools

###########################################################

# データ変換 AA09 START

def AA09_CONV(TEMP_DIR,time1):
    with open(TEMP_DIR + 'aa09.prn', 'r', encoding='cp932') as f:
        AA_STRING1 =f.read()
    LIST1=AA_STRING1.splitlines()
    if len(LIST1) == 0:
        logger.error('LIST1が空です。')
        sys.exit(1)
    LIST1_1=[LIST1[_][:21] for _ in range(4,25)]
    LIST1_2=[LIST1[_][42:53] for _ in range(4,25)]
    LIST1_3=[LIST1[_][59:] for _ in range(4,25)]
    del LIST1_1[2]

    LIST2_1=[]
    LIST2_2=[]
    LIST2_3=[]
    LIST2_1=list(itertools.chain.from_iterable([_.split() for _ in LIST1_1]))
    LIST2_2=list(itertools.chain.from_iterable([_.split() for _ in LIST1_2]))
    LIST2_3=list(itertools.chain.from_iterable([_.split() for _ in LIST1_3]))

    LIST2_3[24]=LIST2_3[24][:-2] #生産m　編集
    LIST2_3[25]=LIST2_3[25][:-2] #起毛反数　編集
    LIST2_3[26]=LIST2_3[26][:-1] #見本m　編集
    del LIST2_3[-1]
    del LIST2_3[22]
    del LIST2_3[14]
    del LIST2_3[7]

    r = re.compile('^[0-9]+$')
    AA_output=[]

    AA_output.append(time1)

    for x in filter(r.match, LIST2_1):
        AA_output.append(x)
    for x in filter(r.match, LIST2_2):
        AA_output.append(x)
    for x in filter(r.match, LIST2_3):
        AA_output.append(x)
    AA_output2 =','.join([str(_) for _ in AA_output])

    # logger.debug('AA_output')
    # print(AA_output)
    # logger.debug('AA_output2')
    # print(AA_output2)

    logger.debug('AA09 data convert finish.')
    return AA_STRING1,AA_output,AA_output2



# データ変換 AA09 END

###########################################################

# データ変換 CC09 START

def CC09_CONV(TEMP_DIR,time1):
    with  open(TEMP_DIR+'cc09.prn', 'r', encoding='cp932') as f:
        CC_STRING1 = f.read()
    CC_LIST1=CC_STRING1.splitlines()
    if len(CC_LIST1) == 0:
        logger.error('CC_LIST1が空です。')
        sys.exit(1)

    # print(CC_LIST1)

    CC_LIST1_1=[CC_LIST1[_][:15] for _ in range(4,24)]
    CC_LIST1_2=[CC_LIST1[_][23:37] for _ in range(4,23)]
    CC_LIST1_3=[CC_LIST1[_][45:] for _ in range(4,23)]

    CC_LIST2_1=[]
    CC_LIST2_2=[]
    CC_LIST2_3=[]
    CC_LIST2_1=list(itertools.chain.from_iterable([_.split() for _ in CC_LIST1_1]))
    CC_LIST2_2=list(itertools.chain.from_iterable([_.split() for _ in CC_LIST1_2]))
    CC_LIST2_3=list(itertools.chain.from_iterable([_.split() for _ in CC_LIST1_3]))

    CC_LIST2_3[67]=CC_LIST2_3[67][:-1] #生産m　編集
    CC_LIST2_3[72]=CC_LIST2_3[72][:-1] #SSB m　編集
    CC_LIST2_3[81]=CC_LIST2_3[81][:-1] #見本m　編集

    del CC_LIST2_3[80] #前から消すと番号がズレるのでけつから消す
    del CC_LIST2_3[76]
    del CC_LIST2_3[71]
    del CC_LIST2_3[66]
    del CC_LIST2_3[60]
    del CC_LIST2_3[54]
    del CC_LIST2_3[48]
    del CC_LIST2_3[41]
    del CC_LIST2_3[34]
    del CC_LIST2_3[17]
    del CC_LIST2_3[9]
    del CC_LIST2_3[3]
    del CC_LIST2_3[54]
    del CC_LIST2_3[16]



    r = re.compile('^[0-9]+$')
    CC_output=[]
    CC_output.append(time1)

    for x in filter(r.match, CC_LIST2_1):
        CC_output.append(x)
    for x in filter(r.match, CC_LIST2_2):
        CC_output.append(x)
    for x in filter(r.match, CC_LIST2_3):
        CC_output.append(x)
    CC_output2 =','.join([str(_) for _ in CC_output])

    # logger.debug('CC_output')
    # print(CC_output)
    # logger.debug('CC_output2')
    # print(CC_output2)

    logger.debug('CC09 data convert finish.')
    return CC_STRING1,CC_output,CC_output2

# データ変換 CC09 END

###########################################################

# データ変換　3K START

def AA3k_CONV(TEMP_DIR,time1):
    with open(TEMP_DIR+'aa3k.prn', 'r', encoding='cp932') as f:
        STRING3_1 =f.read()
    LIST3_1=STRING3_1.splitlines()
    if len(LIST3_1) == 0:
        logger.error('LIST3_1が空です。')
        sys.exit(1)
    LIST3_1_1=[LIST3_1[_].replace(",","") for _ in range(16,18)]
    LIST3_1_2=[LIST3_1[_].replace("/"," ").replace(")"," ").replace(",","").replace("残","残 ") for _ in range(19,25)]

    LIST3_2_1=[]
    LIST3_2_2=[]
    LIST3_2_1=list(itertools.chain.from_iterable([_.split() for _ in LIST3_1_1]))
    LIST3_2_2=[_.split() for _ in LIST3_1_2]
    LIST3_3_2=[_[3:5]+_[8:10]+_[13:15] for _ in LIST3_2_2]
    LIST3_4_2=list(itertools.chain.from_iterable(LIST3_3_2))

    r = re.compile('^[0-9]+$')
    output3_1=[]

    output3_1.append(time1)

    for x in filter(r.match, LIST3_2_1):
        output3_1.append(x)
    for x in filter(r.match, LIST3_4_2):
        output3_1.append(x)
    output3_2 =','.join([str(_) for _ in output3_1])

    # logger.debug('output3_1')
    # print(output3_1)
    # logger.debug('output3_2')
    # print(output3_2)

    logger.debug('AA3K data convert finish.')
    return STRING3_1,output3_1,output3_2

# データ変換　3K END

###########################################################

# データ変換 NN09 START

def NN09_CONV(TEMP_DIR,time1):
    with open(TEMP_DIR + 'nn09.prn', 'r', encoding='cp932') as f:
        NN_STRING1 =f.read()
    LIST1=NN_STRING1.splitlines()
    if len(LIST1) == 0:
        logger.error('LIST1が空です。')
        sys.exit(1)
    LIST1_1=[LIST1[_][:21] for _ in range(4,25)]
    LIST1_2=[LIST1[_][42:53] for _ in range(4,25)]
    LIST1_3=[LIST1[_][59:] for _ in range(4,25)]
    del LIST1_1[2]
    del LIST1_3[14]
    del LIST1_3[7]

    LIST2_1=[]
    LIST2_2=[]
    LIST2_3=[]
    LIST2_1=list(itertools.chain.from_iterable([_.split() for _ in LIST1_1]))
    LIST2_2=list(itertools.chain.from_iterable([_.split() for _ in LIST1_2]))
    LIST2_3=list(itertools.chain.from_iterable([_.split() for _ in LIST1_3]))

    LIST2_3[22]=LIST2_3[22][:-1] #仕上m　編集
    LIST2_3[25]=LIST2_3[25][:-1] #正規仕上m　編集
    LIST2_3[29]=LIST2_3[29][:-1] #再整仕上m　編集
    LIST2_3[33]=LIST2_3[33][:-1] #見本m　編集

    del LIST2_3[-1]
    # del LIST2_3[22]
    # del LIST2_3[14]
    # del LIST2_3[7]

    r = re.compile('^[0-9]+$')
    NN_output=[]

    NN_output.append(time1)

    for x in filter(r.match, LIST2_1):
        NN_output.append(x)
    for x in filter(r.match, LIST2_2):
        NN_output.append(x)
    for x in filter(r.match, LIST2_3):
        NN_output.append(x)
    NN_output2 =','.join([str(_) for _ in NN_output])

    # logger.debug('AA_output')
    # print(AA_output)
    # logger.debug('AA_output2')
    # print(AA_output2)

    logger.debug('nn09 data convert finish.')
    return NN_STRING1,NN_output,NN_output2



# データ変換 NN09 END

###########################################################

# データ変換 AD291 START

def AD291_CONV(TEMP_DIR,time1):
    with open(TEMP_DIR + 'ad291.prn', 'r', encoding='cp932') as f:
        AD_STRING1 =f.read()
    LIST1=AD_STRING1.splitlines()
    if len(LIST1) == 0:
        logger.error('LIST1が空です。')
        sys.exit(1)
    
    LIST1_1=[]

    for _ in range(4,12):
        LIST1_1.append(LIST1[_][9:13])
        LIST1_1.append(LIST1[_][14:18])

    LIST2_1=[]
    LIST2_1=list(itertools.chain.from_iterable([_.split() for _ in LIST1_1]))



    r = re.compile('^[0-9]+$')
    AD_output=[]

    AD_output.append(time1)

    for x in filter(r.match, LIST2_1):
        AD_output.append(x)
    AD_output2 =','.join([str(_) for _ in AD_output])



    logger.debug('ad291 data convert finish.')
    return AD_STRING1,AD_output,AD_output2



# データ変換 AD291 END

###########################################################

# データ変換 NN3L START

def NN3L_CONV(TEMP_DIR, time1):
    # --- PRNファイル読み込み
    file_path = TEMP_DIR + 'nn3l.prn'
    logger.critical(f"NN3L:読み込みファイル名を確認:{file_path}")
    
    with open(TEMP_DIR + 'nn3l.prn', 'r', encoding='cp932') as f:
        NN3L_STRING = f.read()  # ファイル全体を文字列として格納
    LIST1 = NN3L_STRING.splitlines()  # 文字列を行ごとにリスト化
    
    # --- 初期エラーチェック（空ファイルチェック） ---
    if len(LIST1) < 4:
        logger.error('nn3l.prnの行数が不足しています。')
        sys.exit(1)

    LIST1_1 = []
    
    # --- データの切り出し（LIST1_1に格納） ---
    row5 = LIST1[4]
    LIST1_1.append(row5[10:15].strip()) #  (合計)
    LIST1_1.append(row5[15:25].strip()) #  (先染)

    LIST1_1.append(row5[25:30].strip())   #  (後染)
    LIST1_1.append(row5[30:40].strip()) #  (再整)
    
    # --- データの分割とフラット化（LIST2_1に格納） ---
    # 抽出データが数値のみのため、ここでは主に形式を揃える目的
    LIST2_1 = []
    LIST2_1 = list(itertools.chain.from_iterable([_.split() for _ in LIST1_1]))

    # --- 数値のフィルタリングと最終リストの作成 ---
    r = re.compile('^[0-9]+$')  # 数字のみを抽出する正規表現
    NN3L_output = []  # 最終的な出力データリスト
    
    NN3L_output.append(time1)  # 1. タイムスタンプを追加

    # 2. LIST2_1から数字のみの要素をフィルタリングして追加
    for x in filter(r.match, LIST2_1):
        NN3L_output.append(x)
        
    # --- DB挿入用文字列の作成 ---
    # 抽出データをカンマ区切りの文字列に変換
    NN3L_output2 = ','.join([str(_) for _ in NN3L_output])

    # 最終要素数チェックのロギング (想定: 4データ + 1タイムスタンプ = 5)
    if len(NN3L_output) != 5:
        logger.warning(f"NN3L: 最終要素数が想定と異なります（{len(NN3L_output)}/5）。")
        logger.warning(f"NN3L: 抽出されたデータ: {LIST1_1}") # 中間抽出結果もログに出す

    logger.debug('nn3l data convert finish.')
    
    # 元データ文字列、データリスト、カンマ区切り文字列の3つを返す
    return NN3L_STRING, NN3L_output, NN3L_output2

# データ変換 NN3L END

###########################################################
