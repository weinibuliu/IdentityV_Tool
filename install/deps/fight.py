from json import load,loads
from time import sleep,time
from pathlib import Path
from random import randint

from maa.context import Context
from maa.custom_action import CustomAction
from maa.custom_recognition import CustomRecognition

from .infos import base_roi
from .infos import Opera_Singer as o_s

#获取路径
main_path = Path.cwd()

#传出 custom 信息
def rec_name_list() -> list[str]:
    return []
def rec_list() -> list:
    return []
def act_name_list() -> list[str]:
    return ["Fight","o_s_move","o_s_round"]
def act_list() -> list:
    o_s_round = o_s.o_s_round
    o_s_move = o_s.o_s_move
    return [Fight(),o_s_move(),o_s_round()]

def get_roi_base_on_state(roi_state:str):
    match roi_state:
        case "PC16_9":
            roi = base_roi.PC16_9
        case "Android16_9":
            roi = base_roi.Android16_9
        case _:
            raise("roi 声明参数异常，请联系开发者。")
        
    return roi

class Fight(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        
        model = "匹配模式"
        character = "歌剧演员"
        
        def main(model:str,character:str,desktop_notice:bool=False,email_notice:bool=False,
                 limit_reputation:int=75,up2weeklylimit:bool=False,
                 time_limit:bool=False,limit_time:int=0,
                 times_limit:bool=False,limit_times:int=0):
            
            def fight_main(character:str=character):
                fight_start_time = time()
                
                time_diff = 0
                while time_diff < 240:
                    context.run_pipeline("歌剧演员_自定义移动")
                    context.run_action("歌剧演员_移动")
                    
                    a_round_times = randint(5,10)
                    for i in range(a_round_times):
                        context.run_pipeline("歌剧演员_循环")
                        i += 1
                        fight_now_time = time()
                    fight_now_time = time()
                    
                    time_diff = fight_now_time - fight_start_time
                    
                context.run_pipeline("fight_打开设置")

            
            def raedy(model:str=model,character:str=character) -> None:
                context.run_pipeline("fight_点击书")
                sleep(0.5)
                context.run_pipeline(f"fight_{model}")
                sleep(0.5)
                context.run_pipeline("fight_开始匹配")
                context.run_pipeline("Start")
                if model == "排位模式":
                    context.run_pipeline("确认禁用")
                if character == "厂长":
                    context.override_pipeline({"fight_选择角色":{"template": ["characters//厂长.png",
                                                                "characters//厂长_月亮脸.png",
                                                                "characters//厂长_木偶比利.png",
                                                                "characters//厂长_地狱感知.png"]}})
                else:
                    context.override_pipeline({"fight_选择角色":{"template":f"characters//{character}.png"}})
                context.run_pipeline("fight_切换角色")
                
            fight_main(character)    
        
        main(model,character)
        
        return True
    
class Check_reputation(CustomRecognition):
    def analyze(self, context: Context, argv: CustomRecognition.AnalyzeArg) -> CustomRecognition.AnalyzeResult:
        roi_state = loads(argv.custom_recognition_param)["roi_state"]
        roi = get_roi_base_on_state(roi_state)
        
        with open (f"{main_path}/config/fight_config.json") as f:
            lowest = load(f)["信誉分阈值"]

        Get_reputation_pipe = {"Get_reputation":{
            "timeout": 3000,
            "recognition": "OCR",
            "roi": roi.roi_getreputation,
            "only_rec": True
            }}
        
        rec_result = context.run_recognition("Get_reputation",argv.image,pipeline_override = Get_reputation_pipe)
        rec_result = rec_result.best_result.text

        if rec_result < lowest:
            context.override_pipeline({"fight_检测人品值": {"next":["fight_人品值低_桌面提醒"]}})

        return super().analyze(context, argv)