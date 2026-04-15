# tempフォルダ作成モジュール

# logging　config
from logging import getLogger, config
import json
with open('./log_config.json', 'r') as f:
    log_conf = json.load(f)
config.dictConfig(log_conf) #ロギング設定を取得
logger = getLogger(__name__)  #アプリ名でロギング
# logging　config END

import os
# import shutil


def temp_rm_mk(TEMP_DIR):
    # print(__name__)
    # print(TEMP_DIR)
    if not os.path.exists(TEMP_DIR):
        # ディレクトリが存在しない場合、ディレクトリを作成する
        os.makedirs(TEMP_DIR)
        logger.debug('temp folder make')
    # else:
        # tempが残っていたら削除してから作成  
        # ファイルが見つからないときのエラー処理が面倒くさいのでキャンセル
        # shutil.rmtree(TEMP_DIR)
        # os.makedirs(TEMP_DIR)
        # logger.debug('temp folder remake')


