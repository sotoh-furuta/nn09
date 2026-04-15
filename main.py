##################################################
## 
## ETOS AA0090 AA03K2 CC0090 コピースクリプト
## 
##################################################
# import START

import configparser
import json
from logging import getLogger, config
with open('./log_config.json', 'r') as f:
    log_conf = json.load(f)

import datetime
import os

# import END
##################################################
# config and logging START

config.dictConfig(log_conf) #ロギング設定を取得
logger = getLogger(__name__)  #アプリ名でロギング
inifile = configparser.ConfigParser()
inifile.read('./config.ini', 'cp932')

# config and logging END
##################################################
# main START

from ETOS_killer import ETOS_killer
ETOS_killer()

# tempフォルダ作成
path = os.getcwd()
TEMP_DIR = path + '\\temp\\' # フルパスで書くこと
logger.debug('SET temp folder ' + TEMP_DIR)

from my_module  import temp_rm_mk
temp_rm_mk(TEMP_DIR)

# ETOS 起動
from ETOS_OPEN import ETOS_OPEN
p = ETOS_OPEN(TEMP_DIR)
p.kill()

# 日本標準時の取得
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
time1 = "'"+str(now)+"'"

###########################################################
# データ変換 09 START

from ETOS_CONV import AA09_CONV
AA09 = []
AA09 = AA09_CONV(TEMP_DIR,time1)

###########################################################
# データ変換 CC09 START

from ETOS_CONV import CC09_CONV
CC09 = []
CC09 = CC09_CONV(TEMP_DIR,time1)

# データ変換 CC09 END
###########################################################
# データ変換 NN09 START

from ETOS_CONV import NN09_CONV
NN09 = []
NN09 = NN09_CONV(TEMP_DIR,time1)

# データ変換 NN09 END
###########################################################
# データ変換 AD0291 START

from ETOS_CONV import AD291_CONV
AD291 = []
AD291 = AD291_CONV(TEMP_DIR,time1)

# データ変換 AD0291 END
###########################################################
# データ変換　3K START

from ETOS_CONV import AA3k_CONV
AA3K = []
AA3K = AA3k_CONV(TEMP_DIR,time1)

# データ変換　3K END
###########################################################

# データ変換　NN3L START

from ETOS_CONV import NN3L_CONV
NN3L = []
NN3L = NN3L_CONV(TEMP_DIR,time1)

# データ変換　NN3L END
#########################################################

from DB_trancefar import DB_trancefar
DB_trancefar(TEMP_DIR,now,AA09,CC09,NN09,AA3K,AD291,NN3L)

