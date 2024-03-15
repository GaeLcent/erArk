from typing import Tuple, Dict, List
from types import FunctionType
from Script.Core import cache_control, game_type, get_text, flow_handle, constant
from Script.Design import attr_calculation, basement
from Script.UI.Moudle import draw
from Script.Config import game_config, normal_config
from Script.UI.Panel import manage_basement_panel

cache: game_type.Cache = cache_control.cache
""" 游戏缓存数据 """
_: FunctionType = get_text._
""" 翻译api """
line_feed = draw.NormalDraw()
""" 换行绘制对象 """
line_feed.text = "\n"
line_feed.width = 1
window_width: int = normal_config.config_normal.text_width
""" 窗体宽度 """


class Agriculture_Production_Panel:
    """
    用于农业生产的面板对象
    Keyword arguments:
    width -- 绘制宽度
    """

    def __init__(self, width: int):
        """初始化绘制对象"""
        self.width: int = width
        """ 绘制的最大宽度 """
        self.now_panel = _("农业生产")
        """ 当前绘制的页面 """
        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """

    def draw(self):
        """绘制对象"""

        title_text = _("农业生产")
        title_draw = draw.TitleLineDraw(title_text, self.width)

        while 1:
            basement.get_base_updata()
            return_list = []
            title_draw.draw()

            all_info_draw = draw.NormalDraw()
            now_text = ""
            now_text += _(f" 当前仓库等级：{cache.rhodes_island.facility_level[3]}，容量（单资源存放上限）：{cache.rhodes_island.warehouse_capacity}\n")

            # 遍历该类型的资源
            for material_id in [11, 16]:
                material_data  = game_config.config_resouce[material_id]
                now_text += f"  {material_data.name}：{cache.rhodes_island.materials_resouce[material_id]}"
            now_text += "\n"

            all_info_draw.text = now_text
            all_info_draw.width = self.width
            all_info_draw.draw()

            for agriculture_line_id in cache.rhodes_island.agriculture_line:
                now_text = f"\n 药田："
                all_info_draw.text = now_text
                all_info_draw.draw()

                # 基础数据
                resouce_id = cache.rhodes_island.agriculture_line[agriculture_line_id][0]
                resouce_data = game_config.config_resouce[resouce_id]

                # 生产产品
                now_text = _(f"\n    当前生产：{resouce_data.name}(10/d)      ")
                all_info_draw.text = now_text
                all_info_draw.draw()
                button_text = _(" [生产调整] ")
                button_draw = draw.CenterButton(
                    _(button_text),
                    _(f"{button_text}_{agriculture_line_id}"),
                    len(button_text) * 2,
                    cmd_func=self.select_agriculture_line_produce,
                    args=agriculture_line_id,
                    )
                return_list.append(button_draw.return_text)
                button_draw.draw()

                # 生产效率
                now_level = cache.rhodes_island.facility_level[12]
                facility_cid = game_config.config_facility_effect_data["疗养庭院"][int(now_level)]
                all_effect = 0
                facility_effect = game_config.config_facility_effect[facility_cid].effect
                all_effect += facility_effect
                now_text = _(f"\n    当前效率加成：设施(lv{now_level}:{facility_effect}%)")
                # 遍历输出干员的能力效率加成
                for chara_id in cache.rhodes_island.agriculture_line[agriculture_line_id][1]:
                    character_data: game_type.Character = cache.character_data[chara_id]
                    character_effect = int(10 * attr_calculation.get_ability_adjust(character_data.ability[47]))
                    all_effect += character_effect
                    now_text += _(f" + {character_data.name}(农业lv{character_data.ability[47]}:{character_effect}%)")
                now_text += f" = {all_effect}%      "
                all_info_draw.text = now_text
                all_info_draw.draw()
                line_feed.draw()

            line_feed.draw()
            button_text = _("[001]种植员增减")
            button_draw = draw.LeftButton(
                _(button_text),
                _(button_text),
                self.width,
                cmd_func=manage_basement_panel.change_npc_work_out,
                args=self.width
                )

            line_feed.draw()
            back_draw = draw.CenterButton(_("[返回]"), _("返回"), window_width)
            back_draw.draw()
            line_feed.draw()
            return_list.append(back_draw.return_text)
            yrn = flow_handle.askfor_all(return_list)
            if yrn == back_draw.return_text:
                cache.now_panel_id = constant.Panel.IN_SCENE
                break

    def select_agriculture_line_produce(self, agriculture_line_id):
        """选择药田生产的产品"""
        while 1:

                line = draw.LineDraw("-", window_width)
                line.draw()
                info_draw = draw.NormalDraw()
                info_draw.width = window_width
                return_list = []

                now_level = cache.rhodes_island.facility_level[12]
                resouce_id = cache.rhodes_island.agriculture_line[agriculture_line_id][0]
                resouce_data = game_config.config_resouce[resouce_id]

                info_text = f""
                info_text += _(f" 药田当前种植的是：{resouce_data.name}")

                info_text += _("\n\n 当前可以种植的有：\n\n")
                info_draw.text = info_text
                info_draw.draw()

                # 遍历配方列表，获取每个配方的信息
                for cid in [11]:
                    resouce_now_data = game_config.config_resouce[cid]

                    # 判断当前配方是否可以生产，未解锁则跳过
                    flag_open = True
                    # if product_difficulty > now_level:
                    #     flag_open = False

                    if flag_open:

                        # 输出配方信息
                        button_draw = draw.LeftButton(
                            f"[{str(cid).rjust(3,'0')}]{resouce_now_data.name}：{resouce_now_data.info}",
                            f"\n{cid}",
                            window_width ,
                            cmd_func=self.change_agriculture_line_produce,
                            args=(agriculture_line_id ,cid)
                        )
                        button_draw.draw()
                        return_list.append(button_draw.return_text)
                        line_feed.draw()

                line_feed.draw()
                back_draw = draw.CenterButton(_("[返回]"), _("返回"), window_width)
                back_draw.draw()
                line_feed.draw()
                return_list.append(back_draw.return_text)
                yrn = flow_handle.askfor_all(return_list)
                if yrn in return_list:
                    break

    def change_agriculture_line_produce(self, agriculture_line_id, formula_cid):
        """更改药田的种植"""
        if cache.rhodes_island.agriculture_line[agriculture_line_id][0] != 0 and cache.rhodes_island.agriculture_line[agriculture_line_id][4] != cache.game_time.hour:
            pass
        else:
            cache.rhodes_island.agriculture_line[agriculture_line_id][0] = formula_cid
