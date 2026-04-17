# logging　config
from logging import getLogger, config
import json
with open('./log_config.json', 'r') as f:
    log_conf = json.load(f)
config.dictConfig(log_conf) #ロギング設定を取得
logger = getLogger(__name__)  #アプリ名でロギング
# logging　config END

import psycopg2
import configparser
inifile = configparser.ConfigParser()
inifile.read('./config.ini', 'cp932')
import shutil



# AA09 データ出力
def AA09_output(TEMP_DIR,now,cur,conn,AA09):
    logger.debug('AA09 output START')

    table_name = "dai1_tansuu_1min"
    cur.execute('SELECT * FROM "IoT_schema".%s ORDER BY timestamp DESC LIMIT 1'% table_name)
    last_data = list(cur.fetchone()) 
    output3 = [int(x) for x in AA09[1][1:]]
    if last_data[-3] > output3[-3]:
        logger.info("AA09 生産m 減少")
        logger.info('----------output----------')
        logger.info(AA09[1])
        logger.info('----------AA_STRING1----------')
        logger.info(AA09[0])

    if len(AA09[1]) == 88:
        if last_data[1:] != output3:
            cur.execute('INSERT INTO "IoT_schema".%s  VALUES (%s)'% (table_name,AA09[2]))
            conn.commit()   # Auto Commitではないので必ずCommitする
            logger.info('AA09 Data added, recorded in DB.')
        else:
            logger.info('AA09 No data change, not recorded in DB.')
    else:
        logger.error('AA09 要素数不一致のため、データ破棄。')
        logger.info('----------AA09_output----------')
        logger.info(AA09[1])
        logger.info('----------AA09_STRING1----------')
        logger.info(AA09[0])
        shutil.copyfile(TEMP_DIR+'aa09.prn','./error/aa09_'+ now.strftime('%Y%m%d_%H%M%S') +'.prn')

    logger.debug('AA09 output END')




# CC09 データ出力
def CC09_output(TEMP_DIR,now,cur,conn,CC09):
    logger.debug('CC09 output START')

    table_name = "ichinomiya_tansuu_1min"
    cur.execute('SELECT * FROM "IoT_schema".%s ORDER BY timestamp DESC LIMIT 1'% table_name)
    last_data = list(cur.fetchone()) 
    output3 = [int(x) for x in CC09[1][1:]]
    if last_data[-3] > output3[-3]: # 確認
        logger.info("CC 09 生産m 減少") 
        logger.info('----------CC09_output----------')
        logger.info(CC09[1])
        logger.info('----------CC09_STRING1----------')
        logger.info(CC09[0])

    if len(CC09[1]) == 117:
        if last_data[1:] != output3:
            cur.execute('INSERT INTO "IoT_schema".%s  VALUES (%s)'% (table_name,CC09[2]))
            conn.commit()   # Auto Commitではないので必ずCommitする
            logger.info('CC09 Data added, recorded in DB.')
        else:
            logger.info('CC09 No data change, not recorded in DB.')
    else:
        logger.error('CC09 要素数不一致のため、データ破棄。')
        logger.info('----------CC09_output----------')
        logger.info(CC09[1])
        logger.info('----------CC09_STRING1----------')
        logger.info(CC09[0])
        shutil.copyfile(TEMP_DIR+'cc09.prn','./error/cc09_'+ now.strftime('%Y%m%d_%H%M%S') +'.prn')

    logger.debug('CC09 output END')




# NN09 データ出力
def NN09_output(TEMP_DIR,now,cur,conn,NN09):
    logger.debug('NN09 output START')

    table_name = "nikka_tansuu_1min"
    cur.execute('SELECT * FROM "IoT_schema".%s ORDER BY timestamp DESC LIMIT 1'% table_name)
    row = cur.fetchone()
    output3 = [int(x) for x in NN09[1][1:]]
    last_data = None

    if row is not None:
        last_data = list(row)
        # 既存データにNULLが含まれる場合は比較をスキップして継続する
        if last_data[-8] is not None and last_data[-8] > output3[-8]: # 確認
            logger.info("NN 09 生産m 減少")
            logger.info('----------NN09_output----------')
            logger.info(NN09[1])
            logger.info('----------NN09_STRING1----------')
            logger.info(NN09[0])
        elif last_data[-8] is None:
            logger.warning('NN09 比較対象(last_data[-8])がNULLのため、生産m減少チェックをスキップ。')

    if len(NN09[1]) == 90:
        if row is None or last_data is None or last_data[1:] != output3:
            cur.execute('INSERT INTO "IoT_schema".%s  VALUES (%s)'% (table_name,NN09[2]))
            conn.commit()   # Auto Commitではないので必ずCommitする
            logger.info('NN09 Data added, recorded in DB.')
        else:
            logger.info('NN09 No data change, not recorded in DB.')
    else:
        logger.error('NN09 要素数不一致のため、データ破棄。')
        logger.info('----------NN09_output----------')
        logger.info(NN09[1])
        logger.info('----------NN09_STRING1----------')
        logger.info(NN09[0])
        shutil.copyfile(TEMP_DIR+'nn09.prn','./error/nn09_'+ now.strftime('%Y%m%d_%H%M%S') +'.prn')

    logger.debug('NN09 output END')

# AD291 データ出力
def AD291_output(TEMP_DIR,now,cur,conn,AD291):
    logger.debug('AD291 output START')

    table_name = "senshoku_tansuu_1min"
    cur.execute('SELECT * FROM "IoT_schema".%s ORDER BY timestamp DESC LIMIT 1'% table_name)
    last_data = list(cur.fetchone()) 
    output3 = [int(x) for x in AD291[1][1:]]

    if len(AD291[1]) == 17:
        if last_data[1:] != output3:
            cur.execute('INSERT INTO "IoT_schema".%s  VALUES (%s)'% (table_name,AD291[2]))
            conn.commit()   # Auto Commitではないので必ずCommitする
            logger.info('AD291 Data added, recorded in DB.')
        else:
            logger.info('AD291 No data change, not recorded in DB.')
    else:
        logger.error('AD291 要素数不一致のため、データ破棄。')
        logger.info('----------AD291_output----------')
        logger.info(AD291[1])
        logger.info('----------AD291_STRING1----------')
        logger.info(AD291[0])
        shutil.copyfile(TEMP_DIR+'ad291.prn','./error/ad291_'+ now.strftime('%Y%m%d_%H%M%S') +'.prn')

    logger.debug('AD291 output END')


# AA3K データ出力
def AA3K_output(TEMP_DIR,now,cur,conn,AA3K):
    logger.debug('AA3K output START')

    table_name = "dai1_3k_1min"
    cur.execute('SELECT * FROM "IoT_schema".%s ORDER BY timestamp DESC LIMIT 1'% table_name)
    last_data3 = list(cur.fetchone()) 
    output3_3 = [int(x) for x in AA3K[1][1:]]
    if len(AA3K[1]) == 46:
        if last_data3[1:] != output3_3:
            cur.execute('INSERT INTO "IoT_schema".%s  VALUES (%s)'% (table_name,AA3K[2]))
            conn.commit()   # Auto Commitではないので必ずCommitする
            logger.info('AA3K Data added, recorded in DB.')
        else:
            logger.info('AA3K No data change, not recorded in DB.')
    else:
        logger.error('AA3K 要素数不一致のため、データを破棄。')
        # logger.info('----------output3_3----------')
        # logger.info(AA3K[1])
        # logger.info('----------STRING3_1----------')
        # logger.info(AA3K[0])
        # shutil.copyfile(TEMP_DIR+'aa3k.prn','./error/aa3k_'+ now.strftime('%Y%m%d_%H%M%S') +'.prn')

    logger.debug('AA3K output END')

# NN3L データ出力

def NN3L_output(TEMP_DIR,now,cur,conn,NN3L):
    logger.debug('NN3L output START')

    table_name = "nikka_3k_1min"
    cur.execute('SELECT * FROM "IoT_schema".%s ORDER BY timestamp DESC LIMIT 1'% table_name)
    last_data = list(cur.fetchone()) 
    output3 = [int(x) for x in NN3L [1][1:]]
    if len(NN3L[1]) == 5:
        if last_data[1:] != output3:
            cur.execute('INSERT INTO "IoT_schema".%s  VALUES (%s)'% (table_name,NN3L[2]))
            conn.commit()   # Auto Commitではないので必ずCommitする
            logger.info('NN3L Data added, recorded in DB.')
        else:
            logger.info('NN3L No data change, not recorded in DB.')
    else:
        logger.critical('==================== NN3L DEBUG ====================')
        logger.critical(f'DBから取得した最新データ (比較対象): {last_data[1:]}') 
        logger.critical(f'nn3l.prnから読み込んだ新しいデータ: {output3}')
        logger.critical(f'比較結果 (last_data[1:] != output3): {last_data[1:] != output3}')
        logger.critical('====================================================')
        logger.error('NN3L 要素数不一致のため、データ破棄。')
        logger.info('----------NN3L_output----------')
        logger.info(NN3L[1])
        logger.info('----------NN3L_STRING----------')
        logger.info(NN3L[0]) 

        # shutil.copyfile(TEMP_DIR+'nn3l.prn','./error/nn3l_'+ now.strftime('%Y%m%d_%H%M%S') +'.prn')

    logger.debug(' NN3L output END')



# DB出力
def DB_trancefar(TEMP_DIR,now,AA09,CC09,NN09,AA3K,AD291,NN3L):

    # DB接続設定 START
    dbname = inifile.get('DEFAULT','dbname')
    user = inifile.get('DEFAULT','user')
    password = inifile.get('DEFAULT','password')
    host = inifile.get('DEFAULT','host')
    port = inifile.get('DEFAULT','port')
    dsn = "dbname=%s user=%s password=%s host=%s port=%s" % (dbname,user,password,host,port) 
    
    
    # コネクション作成
    with psycopg2.connect(dsn) as conn:
        logger.info('DB Connection Open ')

        # カーソル作成
        with conn.cursor() as cur:
            # DB 接続設定 END

            # AA09 データ出力
            AA09_output(TEMP_DIR,now,cur,conn,AA09)

            # CC09 データ出力
            CC09_output(TEMP_DIR,now,cur,conn,CC09)

            # NN09 データ出力
            NN09_output(TEMP_DIR,now,cur,conn,NN09)

            # AD291 データ出力
            AD291_output(TEMP_DIR,now,cur,conn,AD291)

            # AA3K データ出力
            AA3K_output(TEMP_DIR,now,cur,conn,AA3K)

            # NN3L データ出力
            NN3L_output(TEMP_DIR,now,cur,conn,NN3L)

    logger.info('DB Conection Closed')


    # main END
    ###########################################################
