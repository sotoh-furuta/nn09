import psutil


# ETOSプロセス強制終了 関数
def ETOS_killer():
    for proc in psutil.process_iter():
        # print("----------------------")
        # print("プロセスID:" + str(proc.pid))
        try:
            # print("実行モジュール：" + proc.exe())
            # print("コマンドライン:" + str(proc.cmdline()))
            # print("カレントディレクトリ:" + proc.cwd())
            if "ETOS" in proc.exe() or "ＥＴＯＳ" in proc.exe():
                print("プロセスID:" + str(proc.pid) + "  " + proc.exe() + " is ETOS")
                print("コマンドライン:" + str(proc.cmdline()))
                pid = proc.pid
                p = psutil.Process(pid)
                p.terminate()  # or p.kill()
        except psutil.AccessDenied:
            # print("このプロセスへのアクセス権がありません。")
            pass


ETOS_killer()
