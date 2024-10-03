from pathlib import Path
from maa.toolkit import Toolkit

import deps.ban as ban
import deps.notice as notice

#获取路径
main_path = Path.cwd()

def main():
    # 注册自定义识别器与动作
    rec_names = ban.rec_name_list() + notice.rec_name_list()
    rec_details = ban.rec_list() + notice.rec_list()

    act_names = ban.act_name_list() + notice.act_name_list()
    act_details = ban.act_list() + notice.act_list()
    
    #注册自定义识别器
    for (name,detail) in zip(rec_names,rec_details):
        Toolkit.pi_register_custom_recognition(name,detail)
    
    #注册自定义动作
    for (name,detail) in zip(act_names,act_details):
        Toolkit.pi_register_custom_action(name,detail)

    # 启动 MaaPiCli
    Toolkit.pi_run_cli(f"{main_path}/res", f"{main_path}/debug", False)

if __name__ == "__main__":
    main()