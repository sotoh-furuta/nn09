##################################################
##
## NN09 画面変更対応 デバッグスクリプト
##
## 使い方:
##   python nn09_debug.py              → temp\nn09.prn を検証
##   python nn09_debug.py temp過去     → temp過去\nn09.prn を検証（旧レイアウト）
##   python nn09_debug.py --db         → DB接続して新テーブルの構造も検証
##
##################################################

import sys
import os
import re
import itertools
import configparser

# --- 設定 ---
# 新テーブルのカラム名（timestamp除く、INSERT順）
# ※ 新テーブル作成時に合わせて修正すること
DB_COLUMNS = [
    # 左カラム (LIST2_1) 40個
    "入荷_織_先染","入荷_織_後染","入荷_編_先染","入荷_編_後染",
    "TNY_先染","TNY_後染","AJ_先染","AJ_後染","AJK_先染","AJK_後染",
    "CHS_先染","CHS_後染",
    "MAT_先染","MAT_後染",       # ← 旧:FMT → 新:MAT
    "M-2_先染","M-2_後染",       # ← 旧:MAT → 新:M-2
    "MD_先染","MD_後染",         # ← 旧:M-2 → 新:MD
    "MDO_先染","MDO_後染",       # ← 旧:MD  → 新:MDO（新規）
    "EOL_先染","EOL_後染",
    "PK_先染","PK_後染","MZ_先染","MZ_後染","GS_先染","GS_後染",
    "TD_先染","TD_後染","P_先染","P_後染",
    "P-O_先染","P-O_後染",       # ← 旧:CP → 新:P-O
    "2K_先染","2K_後染","WR_先染","WR_後染","SH_先染","SH_後染",
    # 中カラム (LIST2_2) 30個  ※KD,AF,BLW削除
    "PT_先染","PT_後染","PT3_先染","PT3_後染",
    "CL_先染","CL_後染","CBL_先染","CBL_後染",
    "SBL_先染","SBL_後染","REL_先染","REL_後染",
    "GT_先染","GT_後染","3KJ_先染","3KJ_後染",
    "補修_出_2M","補修_出_3M","補修_戻_2M","補修_戻_3M",
    "仕上_先染","仕上_後染","仕上_正規_先染","仕上_正規_後染",
    "仕上_再整_先染","仕上_再整_後染","出荷_先染","出荷_後染",
    "見本_先染","見本_後染",
    # 右カラム (LIST2_3) 19個
    "L","MF","MR","D","A","SN","NP",
    "色付","当月","2X","3X",
    "仕上m","仕上m_正規","WB_先染","WB_後染",
    "仕上m_再整","WR0_先染","WR0_後染","見本m",
]

EXPECTED_COUNT = 90  # timestamp(1) + データ(89) = 90

# --- 旧テーブル用カラム（比較用） ---
DB_COLUMNS_OLD = [
    "入荷_織_先染","入荷_織_後染","入荷_編_先染","入荷_編_後染",
    "TNY_先染","TNY_後染","AJ_先染","AJ_後染","AJK_先染","AJK_後染",
    "CHS_先染","CHS_後染",
    "FMT_先染","FMT_後染","MAT_先染","MAT_後染",
    "M-2_先染","M-2_後染","MD_先染","MD_後染",
    "EOL_先染","EOL_後染",
    "PK_先染","PK_後染","MZ_先染","MZ_後染","GS_先染","GS_後染",
    "TD_先染","TD_後染","P_先染","P_後染",
    "CP_先染","CP_後染",
    "2K_先染","2K_後染","WR_先染","WR_後染","SH_先染","SH_後染",
    "PT_先染","PT_後染","PT3_先染","PT3_後染",
    "CL_先染","CL_後染","CBL_先染","CBL_後染",
    "SBL_先染","SBL_後染",
    "KD_先染","KD_後染","AF_先染","AF_後染","REL_先染","REL_後染",
    "BLW_先染","BLW_後染",
    "GT_先染","GT_後染","3KJ_先染","3KJ_後染",
    "補修_出_2M","補修_出_3M","補修_戻_2M","補修_戻_3M",
    "仕上_先染","仕上_後染","仕上_正規_先染","仕上_正規_後染",
    "仕上_再整_先染","仕上_再整_後染","出荷_先染","出荷_後染",
    "見本_先染","見本_後染",
    "L","MF","MR","D","A","SN","NP",
    "色付","当月","2X","3X",
    "仕上m","仕上m_正規","WB_先染","WB_後染",
    "仕上m_再整","WR0_先染","WR0_後染","見本m",
]


def separator(title=""):
    print("=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)


def step1_read_prn(filepath):
    """Step1: PRNファイル読み込み"""
    separator("Step1: PRNファイル読み込み")
    print(f"  ファイル: {filepath}")

    if not os.path.exists(filepath):
        print(f"  [ERROR] ファイルが存在しません: {filepath}")
        return None

    with open(filepath, 'r', encoding='cp932') as f:
        raw = f.read()

    lines = raw.splitlines()
    print(f"  総行数: {len(lines)}")
    print()
    print("  --- データ領域 (行4-24, 0始まり) ---")
    for i in range(4, min(26, len(lines))):
        print(f"  [{i:2d}] |{lines[i]}|")
    print()
    return lines


def step2_extract_columns(lines):
    """Step2: 3カラム切り出し"""
    separator("Step2: 3カラムの切り出し")

    LIST1_1 = [lines[_][:21]   for _ in range(4, 25)]
    LIST1_2 = [lines[_][42:53] for _ in range(4, 25)]
    LIST1_3 = [lines[_][59:]   for _ in range(4, 25)]

    print("  --- LIST1_1 (左カラム [:21]) 削除前 ---")
    for i, v in enumerate(LIST1_1):
        marker = " ← del" if i == 2 else ""
        print(f"  [{i:2d}] |{v}|{marker}")

    del LIST1_1[2]

    print()
    print("  --- LIST1_3 (右カラム [59:]) 削除前 ---")
    for i, v in enumerate(LIST1_3):
        marker = ""
        if i == 14:
            marker = " ← del(1回目)"
        elif i == 7:
            marker = " ← del(2回目)"
        print(f"  [{i:2d}] |{v}|{marker}")

    del LIST1_3[14]
    del LIST1_3[7]

    return LIST1_1, LIST1_2, LIST1_3


def step3_flatten(LIST1_1, LIST1_2, LIST1_3):
    """Step3: トークン分割とフラット化"""
    separator("Step3: トークン分割・フラット化・単位除去")

    LIST2_1 = list(itertools.chain.from_iterable([_.split() for _ in LIST1_1]))
    LIST2_2 = list(itertools.chain.from_iterable([_.split() for _ in LIST1_2]))
    LIST2_3 = list(itertools.chain.from_iterable([_.split() for _ in LIST1_3]))

    print(f"  LIST2_1: {len(LIST2_1)}トークン")
    print(f"  LIST2_2: {len(LIST2_2)}トークン")
    print(f"  LIST2_3: {len(LIST2_3)}トークン")
    print()

    # 単位除去
    print("  --- LIST2_3 単位除去 ---")
    edits = {22: "仕上m", 25: "仕上m_正規", 29: "仕上m_再整", 33: "見本m"}
    for idx, label in edits.items():
        if idx < len(LIST2_3):
            before = LIST2_3[idx]
            LIST2_3[idx] = LIST2_3[idx][:-1]
            print(f"  [{idx}] {label}: |{before}| → |{LIST2_3[idx]}|")
        else:
            print(f"  [{idx}] {label}: [ERROR] インデックス範囲外 (LIST2_3は{len(LIST2_3)}個)")

    # 末尾削除
    if LIST2_3:
        print(f"  del [-1]: |{LIST2_3[-1]}| を削除")
        del LIST2_3[-1]

    print()
    print("  --- LIST2_3 全トークン一覧 ---")
    for i, v in enumerate(LIST2_3):
        print(f"  [{i:2d}] |{v}|")

    return LIST2_1, LIST2_2, LIST2_3


def step4_filter_and_output(LIST2_1, LIST2_2, LIST2_3):
    """Step4: 数値フィルタリングと最終出力"""
    separator("Step4: 数値フィルタリング")

    r = re.compile('^[0-9]+$')
    nums_1 = list(filter(r.match, LIST2_1))
    nums_2 = list(filter(r.match, LIST2_2))
    nums_3 = list(filter(r.match, LIST2_3))

    print(f"  LIST2_1: {len(LIST2_1)}トークン → {len(nums_1)}個の数値")
    print(f"  LIST2_2: {len(LIST2_2)}トークン → {len(nums_2)}個の数値")
    print(f"  LIST2_3: {len(LIST2_3)}トークン → {len(nums_3)}個の数値")

    all_nums = nums_1 + nums_2 + nums_3
    total = 1 + len(all_nums)  # timestamp + data
    print()
    print(f"  合計: timestamp(1) + データ({len(all_nums)}) = {total}")
    print(f"  期待値: {EXPECTED_COUNT}")

    if total == EXPECTED_COUNT:
        print(f"  [OK] 要素数一致")
    else:
        print(f"  [NG] 要素数不一致! 差分: {total - EXPECTED_COUNT}")

    return nums_1, nums_2, nums_3, total


def step5_column_mapping(nums_1, nums_2, nums_3, total):
    """Step5: DBカラムとの対応表示"""
    separator("Step5: DBカラム対応マッピング")

    all_nums = nums_1 + nums_2 + nums_3

    # 新テーブル用マッピング
    columns = DB_COLUMNS
    if total == 96:
        print("  ※ 旧レイアウト(96列)検出 → 旧テーブルカラム名で表示")
        columns = DB_COLUMNS_OLD

    print(f"  カラム定義数: {len(columns)}")
    print(f"  データ数:     {len(all_nums)}")
    print()

    if len(all_nums) != len(columns):
        print(f"  [NG] データ数({len(all_nums)})とカラム数({len(columns)})が不一致!")
        print()

    # セクション表示
    sections = [
        ("左カラム (LIST2_1)", nums_1, 0),
        ("中カラム (LIST2_2)", nums_2, len(nums_1)),
        ("右カラム (LIST2_3)", nums_3, len(nums_1) + len(nums_2)),
    ]

    for section_name, nums, offset in sections:
        print(f"  --- {section_name} ({len(nums)}個) ---")
        for i, val in enumerate(nums):
            col_idx = offset + i
            col_name = columns[col_idx] if col_idx < len(columns) else "???"
            print(f"  [{col_idx+1:3d}] {col_name:20s} = {val}")
        print()


def step6_db_check():
    """Step6: DB接続してテーブル構造を確認"""
    separator("Step6: DB テーブル構造検証")

    try:
        import psycopg2
    except ImportError:
        print("  [SKIP] psycopg2がインストールされていません")
        return

    inifile = configparser.ConfigParser()
    inifile.read('./config.ini', 'cp932')
    try:
        dbname = inifile.get('DEFAULT', 'dbname').strip("'")
        user = inifile.get('DEFAULT', 'user').strip("'")
        password = inifile.get('DEFAULT', 'password').strip("'")
        host = inifile.get('DEFAULT', 'host').strip("'")
        port = inifile.get('DEFAULT', 'port').strip("'")
    except Exception as e:
        print(f"  [ERROR] config.ini読み込み失敗: {e}")
        return

    dsn = f"dbname={dbname} user={user} password={password} host={host} port={port}"
    print(f"  接続先: {host}:{port}/{dbname}")

    try:
        with psycopg2.connect(dsn, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                # テーブル存在確認
                cur.execute("""
                    SELECT column_name, data_type, ordinal_position
                    FROM information_schema.columns
                    WHERE table_schema = 'IoT_schema'
                      AND table_name = 'nikka_tansuu_1min'
                    ORDER BY ordinal_position
                """)
                rows = cur.fetchall()
                if not rows:
                    print("  [NG] テーブル nikka_tansuu_1min が存在しません")
                    return

                print(f"  テーブルカラム数: {len(rows)} (timestamp含む)")
                print(f"  期待カラム数:     {EXPECTED_COUNT} (timestamp含む)")
                print()

                if len(rows) != EXPECTED_COUNT:
                    print(f"  [NG] カラム数不一致!")
                    print()

                print("  --- テーブルカラム一覧 ---")
                for col_name, data_type, pos in rows:
                    # 新テーブルカラムとの照合
                    expected = ""
                    if pos == 1:
                        expected = "(timestamp)"
                    elif pos - 2 < len(DB_COLUMNS):
                        expected = DB_COLUMNS[pos - 2]

                    match = "  " if col_name == expected or pos == 1 else "!!"
                    print(f"  {match} [{pos:3d}] {col_name:25s} ({data_type})")

                # 行数確認
                cur.execute('SELECT COUNT(*) FROM "IoT_schema".nikka_tansuu_1min')
                count = cur.fetchone()[0]
                print(f"\n  テーブル行数: {count}")
                if count == 0:
                    print("  [WARN] テーブルが空です → fetchone()がNoneを返します")

    except Exception as e:
        print(f"  [ERROR] DB接続失敗: {e}")


def main():
    # 引数処理
    target_dir = "temp"
    do_db_check = False

    for arg in sys.argv[1:]:
        if arg == "--db":
            do_db_check = True
        else:
            target_dir = arg

    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, target_dir, "nn09.prn")

    print()
    print("  NN09 画面変更対応 デバッグツール")
    print(f"  対象: {filepath}")
    if do_db_check:
        print("  DB検証: ON")
    print()

    # Step1
    lines = step1_read_prn(filepath)
    if lines is None:
        return

    # Step2
    LIST1_1, LIST1_2, LIST1_3 = step2_extract_columns(lines)

    # Step3
    LIST2_1, LIST2_2, LIST2_3 = step3_flatten(LIST1_1, LIST1_2, LIST1_3)

    # Step4
    nums_1, nums_2, nums_3, total = step4_filter_and_output(LIST2_1, LIST2_2, LIST2_3)

    # Step5
    step5_column_mapping(nums_1, nums_2, nums_3, total)

    # Step6 (オプション)
    if do_db_check:
        step6_db_check()

    # 最終サマリ
    separator("サマリ")
    if total == EXPECTED_COUNT:
        print(f"  [OK] 抽出データ {total}件 → DB挿入可能")
    else:
        print(f"  [NG] 抽出データ {total}件 (期待値 {EXPECTED_COUNT})")
        print(f"       ETOS_CONV.py または DB テーブルの修正が必要")
    print()


if __name__ == "__main__":
    main()
