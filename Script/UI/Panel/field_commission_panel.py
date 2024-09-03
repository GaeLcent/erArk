from typing import Tuple, List
from types import FunctionType
from Script.Core import cache_control, game_type, get_text, flow_handle, constant
from Script.UI.Moudle import draw, panel
from Script.Config import game_config, normal_config
from Script.Design import game_time
from Script.Settle import default

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

def get_commission_demand_and_reward(commission_id: int, send_npc_list = [], demand_or_reward: bool = False, deduction_or_increase: bool = False) -> List:
    """
    获取委托需求或奖励\n
    Keyword arguments:\n
    commission_id -- 委托编号\n
    send_npc_list -- 派遣人员列表，默认为空\n
    demand_or_reward -- False为需求，True为奖励，默认为False\n
    deduction -- 是否扣除或增加资源，默认为False\n
    Return arguments:\n
    return_list -- [是否满足, 需求类型文本, 需求全文]
    """
    commission_data = game_config.config_commission[commission_id]
    # 获取需求或奖励文本
    if demand_or_reward == False:
        all_text = commission_data.demand
    else:
        all_text = commission_data.reward
    # 文本可能以“&”分隔
    if "&" in all_text:
        text_list = all_text.split("&")
    else:
        text_list = [all_text]
    # 初始化变量
    satify_flag = True # 是否满足
    type_text = "" # 类型文本
    full_text = "" # 全文

    # 遍历文本列表
    for now_text in text_list:
        type_text, full_text, satify_flag = process_commission_text(now_text, demand_or_reward, deduction_or_increase, send_npc_list, type_text, full_text, satify_flag)

    return_list = [satify_flag, type_text, full_text]
    return return_list


def process_commission_text(now_text, demand_or_reward, deduction_or_increase, send_npc_list, type_text, full_text, satify_flag):
    """
    处理委托文本\n
    Keyword arguments:\n
    now_text -- 当前文本\n
    demand_or_reward -- False为需求，True为奖励\n
    deduction_or_increase -- 是否扣除或增加资源\n
    send_npc_list -- 派遣人员列表\n
    type_text -- 类型文本\n
    full_text -- 全文\n
    satify_flag -- 是否满足\n
    Return arguments:\n
    type_text -- 类型文本\n
    full_text -- 全文\n
    satify_flag -- 是否满足
    """

    # 处理文本
    text_list = now_text.split("_")
    item_id = int(text_list[1])
    item_num = int(text_list[2])

    # 资源
    if text_list[0] == "r":
        item_name = game_config.config_resouce[item_id].name
        item_type = game_config.config_resouce[item_id].type
        now_have_item_num = cache.rhodes_island.materials_resouce[item_id]
    # 能力
    elif text_list[0] == "a":
        item_name = game_config.config_ability[item_id].name
        item_type = item_name
        now_have_item_num = sum(cache.character_data[character_id].ability[item_id] for character_id in send_npc_list)
    # 经验
    elif text_list[0] == "e":
        item_name = game_config.config_experience[item_id].name
        item_type = item_name
        # 如果是奖励，则只显示大类
        if demand_or_reward:
            item_type = _("经验")
        now_have_item_num = sum(cache.character_data[character_id].experience[item_id] for character_id in send_npc_list)
    # 委托
    elif text_list[0] == "m":
        item_name = _("委托")
        item_type = _("委托")
    # 特产
    elif text_list[0] == _("特产"):
        # 默认值
        item_name = _("特产")
        item_type = _("特产")
        now_have_item_num = 0
        # 获取当前地点的特产
        now_location = cache.rhodes_island.current_location[0]
        nation_specialty_list = game_config.config_resouce_data_of_nation.get(now_location, [])
        # 如果有特产的话，获取特产数量
        if len(nation_specialty_list):
            item_id = nation_specialty_list[0]
            item_name = game_config.config_resouce[item_id].name
            now_have_item_num = cache.rhodes_island.materials_resouce[item_id]
    # 声望
    elif text_list[0] == _("声望"):
        item_name = _("声望")
        item_type = _("声望")
        # 0为当前国家
        if item_id == 0:
            now_country = cache.rhodes_island.current_location[0]
            for nation_id in game_config.config_nation_data_of_country_subordinate:
                nation_data = game_config.config_nation[nation_id]
                if nation_data.country == now_country:
                    item_id = nation_id
                    item_name = nation_data.name + _("声望")
                    now_have_item_num = cache.country.nation_reputation[nation_id]
                    break
        else:
            item_name = game_config.config_nation[item_id].name + _("声望")
            now_have_item_num = cache.country.nation_reputation[item_id]

    # 需求
    if not demand_or_reward:
        # 如果不够数量，设为不满足
        if now_have_item_num < item_num:
            satify_flag = False
        else:
            # 扣除资源
            if deduction_or_increase and text_list[0] == "r":
                cache.rhodes_island.materials_resouce[item_id] -= item_num
            elif deduction_or_increase and text_list[0] == "声望":
                item_num *= 0.01
                cache.country.nation_reputation[item_id] -= item_num
    # 奖励
    else:
        # 增加资源
        if deduction_or_increase:
            # 资源
            if text_list[0] == "r":
                cache.rhodes_island.materials_resouce[item_id] += item_num
            # 经验
            elif text_list[0] == "e":
                for character_id in send_npc_list:
                    cache.character_data[character_id].experience[item_id] += item_num
            # 特产
            elif text_list[0] == "特产":
                cache.rhodes_island.materials_resouce[item_id] += item_num
            # 委托部分，-1不可完成，0可以进行，1已完成
            elif text_list[0] == "m":
                if item_num == -1:
                    cache.rhodes_island.shut_down_field_commissions_set.add(item_id)
                elif item_num == 0:
                    if item_id in cache.rhodes_island.shut_down_field_commissions_set:
                        cache.rhodes_island.shut_down_field_commissions_set.remove(item_id)
                    elif item_id in cache.rhodes_island.finished_field_commissions_set:
                        cache.rhodes_island.finished_field_commissions_set.remove(item_id)
                elif item_num == 1:
                    cache.rhodes_island.finished_field_commissions_set.add(item_id)
            # 声望
            elif text_list[0] == "声望":
                item_num *= 0.01
                cache.country.nation_reputation[item_id] += item_num

    # 添加类型文本
    if item_type not in type_text:
        type_text += f"{item_type} "

    # 添加全文
    if not demand_or_reward:
        full_text += f"{item_name}:{now_have_item_num}/{item_num} "
    else:
        full_text += f"{item_name}:{item_num} "

    return type_text, full_text, satify_flag


def update_field_commission():
    """
    刷新外勤委托的相关数据
    """
    judge_field_commission_finish()
    find_nation_field_commission()


def judge_field_commission_finish():
    """
    判断外勤委托是否完成
    """

    import random

    now_time = cache.game_time
    now_ongoing_field_commissions = cache.rhodes_island.ongoing_field_commissions.copy()
    draw_text = ""
    for commision_id in now_ongoing_field_commissions:
        end_time = cache.rhodes_island.ongoing_field_commissions[commision_id][1]
        if game_time.judge_date_big_or_small(now_time, end_time) or game_time.count_day_for_datetime(now_time, end_time) == 0:
            # 获取奖励
            reward_return_list = get_commission_demand_and_reward(commision_id, [], True, True)
            reward_text = reward_return_list[2]
            # 加入已完成的委托
            if commision_id not in cache.rhodes_island.finished_field_commissions_set:
                cache.rhodes_island.finished_field_commissions_set.add(commision_id)
            # 奖励信息
            commision_name = game_config.config_commission[commision_id].name
            draw_text += "\n"
            # 派遣人员上线
            send_npc_list = cache.rhodes_island.ongoing_field_commissions[commision_id][0]
            for character_id in send_npc_list:
                cache.character_data[character_id].sp_flag.field_commission = 0
                default.handle_chara_on_line(character_id, 1, change_data = game_type.CharacterStatusChange, now_time = cache.game_time)
                draw_text += f"{cache.character_data[character_id].name} "
            # 载具回收
            send_vehicle_list = cache.rhodes_island.ongoing_field_commissions[commision_id][2]
            for vehicle_id in send_vehicle_list:
                # 20%概率载具损坏
                if random.randint(1, 5) == 1:
                    cache.rhodes_island.vehicles[vehicle_id][0] += -1
                    cache.rhodes_island.vehicles[vehicle_id][1] += -1
                    draw_text += _("({0}损坏)").format(game_config.config_vehicle[vehicle_id].name)
                else:
                    cache.rhodes_island.vehicles[vehicle_id][1] -= 1
            draw_text += _("完成了委托：{0}，获得奖励：{1}\n\n").format(commision_name, reward_text)
            # 移除委托
            cache.rhodes_island.ongoing_field_commissions.pop(commision_id)

    # 绘制完成委托
    if len(draw_text):
        info_draw = draw.WaitDraw()
        info_draw.text = draw_text
        info_draw.style = "gold_enrod"
        info_draw.width = window_width
        info_draw.draw()


def find_nation_field_commission():
    """
    寻找来自势力的外勤委托
    Keyword arguments:
    Return arguments:
    """
    # TODO: 未实装


class Field_Commission_Panel:
    """
    用于显示外勤委托界面面板对象
    Keyword arguments:
    width -- 绘制宽度
    """

    def __init__(self, width: int):
        """初始化绘制对象"""
        self.width: int = width
        """ 绘制的最大宽度 """
        self.now_panel = _("常规外勤")
        """ 当前绘制的页面 """
        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.send_npc_list = []
        """ 派遣人员列表 """
        self.send_vehicle_dict = {}
        """ 派遣载具字典 """

    def draw(self):
        """绘制对象"""

        title_text = _("外勤委托")
        commission_type_list = [_("常规外勤"), _("特殊外勤")]

        title_draw = draw.TitleLineDraw(title_text, self.width)
        while 1:
            return_list = []
            title_draw.draw()

            # 绘制面板类型切换
            for commission_type in commission_type_list:
                if commission_type == self.now_panel:
                    now_draw = draw.CenterDraw()
                    now_draw.text = f"[{commission_type}]"
                    now_draw.style = "onbutton"
                    now_draw.width = self.width / len(commission_type_list)
                    now_draw.draw()
                else:
                    now_draw = draw.CenterButton(
                        f"[{commission_type}]",
                        f"\n{commission_type}",
                        self.width / len(commission_type_list),
                        cmd_func=self.change_panel,
                        args=(commission_type,),
                    )
                    now_draw.draw()
                    return_list.append(now_draw.return_text)
            line_feed.draw()
            line = draw.LineDraw("+", self.width)
            line.draw()

            # 绘制提示信息
            info_text_list = ["委托等级", "委托名称", "派遣人数", "耗时天数", "需求类型", "奖励类型"]
            for info_text in info_text_list:
                info_draw = draw.CenterDraw()
                info_draw.text = info_text
                info_draw.width = self.width / len(info_text_list)
                info_draw.draw()
            line_feed.draw()
            line = draw.LineDraw("~", self.width)
            line.draw()

            # 获取当前国家的委托列表
            now_country_id = cache.rhodes_island.current_location[0]
            if now_country_id in game_config.config_commission_id_by_country:
                now_country_commision_list = game_config.config_commission_id_by_country[now_country_id]
            else:
                now_country_commision_list = []
            common_commision_list = game_config.config_commission_id_by_country[-1]
            all_commision_list = now_country_commision_list + common_commision_list

            # 绘制委托信息
            for commision_id in all_commision_list:
                commision_data = game_config.config_commission[commision_id]
                # 跳过非当前面板的委托
                if self.now_panel == _("常规外勤") and commision_data.special != 0:
                    continue
                if self.now_panel == _("特殊外勤") and commision_data.special == 0:
                    continue
                # 跳过未满足前置委托的委托
                if commision_data.related_id != -1 and commision_data.related_id not in cache.rhodes_island.finished_field_commissions_set:
                    continue
                # 特殊外勤只能接受一次
                if commision_data.special != 0 and commision_id in cache.rhodes_island.finished_field_commissions_set:
                    continue
                # 跳过已经关闭的委托
                if commision_id in cache.rhodes_island.shut_down_field_commissions_set:
                    continue
                # 委托信息
                commision_name = commision_data.name
                commision_level = str(commision_data.level)
                commision_people = str(commision_data.people) + _("人")
                commision_time = str(commision_data.time) + _("天")
                demand_return_list = get_commission_demand_and_reward(commision_id, self.send_npc_list)
                commision_demand = demand_return_list[1]
                reward_return_list = get_commission_demand_and_reward(commision_id, self.send_npc_list, True)
                commision_reward = reward_return_list[1]
                # 修正文本宽度
                text_width = int(self.width / (len(info_text_list)))
                str_text_width = int(text_width / 2)
                # 最终文本
                commision_text = f"{commision_level.center(text_width,' ')}{commision_name.center(str_text_width,'　')}{commision_people.center(text_width,' ')}{commision_time.center(text_width,' ')}{commision_demand.center(str_text_width,'　')}{commision_reward.center(str_text_width,'　')}"

                # 可以进行的，绘制为按钮
                if commision_id not in cache.rhodes_island.ongoing_field_commissions:
                    commision_draw = draw.LeftButton(
                        commision_text,
                        "\n" + commision_name,
                        self.width,
                        cmd_func=self.commision_info,
                        args=(commision_id,),
                    )
                    commision_draw.draw()
                    return_list.append(commision_draw.return_text)
                # 正在进行的，绘制为灰色文字
                else:
                    commision_draw = draw.NormalDraw()
                    commision_text = _("(进行中)") + commision_text
                    commision_draw.text = commision_text
                    commision_draw.width = self.width
                    commision_draw.style = "deep_gray"
                    commision_draw.draw()
                line_feed.draw()

            line_feed.draw()
            back_draw = draw.CenterButton(_("[返回]"), _("返回"), window_width)
            back_draw.draw()
            return_list.append(back_draw.return_text)
            yrn = flow_handle.askfor_all(return_list)
            if yrn == back_draw.return_text:
                cache.now_panel_id = constant.Panel.IN_SCENE
                break

    def change_panel(self, building_type: str):
        """
        切换当前面板显示
        Keyword arguments:
        building_type -- 要切换的面板类型
        """

        self.now_panel = building_type

    def commision_info(self, commision_id: int):
        """
        显示委托详细信息
        Keyword arguments:
        commision_id -- 委托编号
        """

        # 委托信息
        commision_data = game_config.config_commission[commision_id]
        commision_name = commision_data.name
        commision_level = str(commision_data.level)
        commision_people = str(commision_data.people) + _("人")
        commision_time = str(commision_data.time) + _("天")
        commision_capacity_int = (commision_data.time - 1) * commision_data.people
        commision_capacity_str = _(" {0}(天数-1) * {1}(人数) = {2}").format(commision_data.time - 1, commision_data.people, commision_capacity_int)
        reward_return_list = get_commission_demand_and_reward(commision_id, self.send_npc_list, True)
        commision_reward = reward_return_list[1]
        commision_description = commision_data.description
        # 将\n替换为换行符
        if "\\n" in commision_description:
            commision_description = commision_description.replace("\\n", "\n      ")

        # 派遣人员与载具
        self.send_npc_list = []
        self.send_vehicle_dict = {}

        while 1:
            # 是否满足条件
            all_satisfy = True
            # 获取需求
            demand_return_list = get_commission_demand_and_reward(commision_id, self.send_npc_list)
            commision_demand = demand_return_list[2]
            deman_satify = demand_return_list[0]

            return_list = []
            line = draw.LineDraw("-", self.width)
            line.draw()

            # 绘制委托信息
            info_draw = draw.NormalDraw()
            info_draw.text = _("\n委托名称：{0}").format(commision_name)
            info_draw.text += _("\n委托等级：{0}").format(commision_level)
            info_draw.text += _("\n派遣人数：{0}").format(commision_people)
            info_draw.text += _("\n耗时天数：{0}").format(commision_time)
            info_draw.text += _("\n载具运量需求：{0}").format(commision_capacity_str)
            info_draw.text += _("\n其他需求：{0}").format(commision_demand)
            info_draw.text += _("\n奖励：{0}").format(commision_reward)
            info_draw.text += _("\n介绍：{0}").format(commision_description)
            info_draw.width = self.width
            info_draw.draw()

            # 绘制派遣人员与载具是否满足需求
            info_draw_2_text = _("\n\n派遣人员：")
            for chara_id in self.send_npc_list:
                chara_data = cache.character_data[chara_id]
                chara_name = chara_data.name
                info_draw_2_text += f"  {chara_name}"
            info_draw_2_text += _("\n\n派遣载具：")
            now_capacity = 0 # 当前运载量
            for vehicle_id in self.send_vehicle_dict:
                vehicle_name = game_config.config_vehicle[vehicle_id].name
                info_draw_2_text += f"  {vehicle_name} * {self.send_vehicle_dict[vehicle_id]}"
                now_capacity += game_config.config_vehicle[vehicle_id].capacity * self.send_vehicle_dict[vehicle_id]
            info_draw_2_text += _("  总运载量：{0}").format(now_capacity)
            info_draw_2_text += _("\n\n是否满足需求：")
            # 人数需求
            info_draw_2_text += _("人数需求：")
            if len(self.send_npc_list) >= commision_data.people:
                info_draw_2_text += "√"
            else:
                all_satisfy = False
                info_draw_2_text += "X"
            # 载具需求
            info_draw_2_text += _("  载具需求：")
            if now_capacity >= commision_capacity_int:
                info_draw_2_text += "√"
            else:
                all_satisfy = False
                info_draw_2_text += "X"
            # 其他需求
            info_draw_2_text += _("  其他需求：")
            if deman_satify:
                info_draw_2_text += "√"
            else:
                all_satisfy = False
                info_draw_2_text += "X"
            info_draw_2 = draw.NormalDraw()
            info_draw_2.text = info_draw_2_text
            info_draw_2.width = self.width
            info_draw_2.draw()

            # 调整派遣人员
            line_feed.draw()
            line_feed.draw()
            adjust_NPC_button_draw = draw.CenterButton(
                _("【调整派遣人员】"),
                _("\n【调整派遣人员】"),
                self.width / 3,
                cmd_func=self.adjust_send_npc,
                args=(commision_id,),
            )
            adjust_NPC_button_draw.draw()
            return_list.append(adjust_NPC_button_draw.return_text)

            # 调整使用载具
            adjust_vehicle_button_draw = draw.CenterButton(
                _("【调整使用载具】"),
                _("\n【调整使用载具】"),
                self.width / 3,
                cmd_func=self.adjust_send_vehicle,
                args=(commision_capacity_int,),
            )
            adjust_vehicle_button_draw.draw()
            return_list.append(adjust_vehicle_button_draw.return_text)
            line_feed.draw()
            line_feed.draw()

            line_feed.draw()
            yes_draw = draw.CenterButton(
                _("[执行委托]"),
                ("\n执行委托"),
                self.width / 2,
                cmd_func=self.send_commision,
                args=(commision_id,),
            )
            if all_satisfy:
                yes_draw.draw()
                return_list.append(yes_draw.return_text)

            back_draw = draw.CenterButton(_("[返回]"), _("返回"), self.width / 2)
            back_draw.draw()
            return_list.append(back_draw.return_text)
            yrn = flow_handle.askfor_all(return_list)
            if yrn == yes_draw.return_text or yrn == back_draw.return_text:
                break

    def adjust_send_npc(self, commision_id: int):
        """
        调整派遣人员
        Keyword arguments:
        commision_id -- 委托编号
        """

        commision_data = game_config.config_commission[commision_id]
        commision_people = commision_data.people

        while 1:
            return_list = []
            line = draw.LineDraw("-", self.width)
            line.draw()

            # 绘制可派遣人员
            info_draw_2 = draw.NormalDraw()
            info_draw_2.text = _("\n可派遣人员（需要{0}人）：\n\n").format(commision_people)
            info_draw_2.width = self.width
            info_draw_2.draw()
            npc_draw_count = 0
            for character_id in cache.npc_id_got:
                draw_style = "standard"
                # 如果已经选择，则绘制为金色
                if character_id in self.send_npc_list:
                    draw_style = "gold_enrod"
                character_data: game_type.Character = cache.character_data[character_id]
                character_name = character_data.name
                character_adv = character_data.adv
                draw_text = f"[{str(character_adv).rjust(4,'0')}]{character_name}"

                # 如果可以选择，则正常绘制按钮
                if len(self.send_npc_list) < commision_people or character_id in self.send_npc_list:
                    button_draw = draw.LeftButton(
                        draw_text,
                        f"\n{character_id}",
                        self.width / 6 ,
                        normal_style = draw_style,
                        cmd_func = self.select_this_npc,
                        args=character_id,
                    )
                    button_draw.draw()
                    return_list.append(button_draw.return_text)
                # 如果当前人数已经满足，则不再绘制按钮，只绘制文本
                else:
                    info_draw = draw.LeftDraw()
                    info_draw.text = draw_text
                    info_draw.width = self.width / 6
                    info_draw.style = "deep_gray"
                    info_draw.draw()

                # 每绘制6个角色换行
                npc_draw_count += 1
                if npc_draw_count % 6 == 0:
                    line_feed.draw()

            line_feed.draw()
            line_feed.draw()
            back_draw = draw.CenterButton(_("[返回]"), _("返回"), window_width)
            back_draw.draw()
            return_list.append(back_draw.return_text)
            yrn = flow_handle.askfor_all(return_list)
            if yrn == back_draw.return_text:
                break


    def adjust_send_vehicle(self, commision_capacity_int: int):
        """
        调整派遣载具
        Keyword arguments:
        commision_capacity_int -- 需要的载具运量
        """

        while 1:
            return_list = []
            line = draw.LineDraw("-", self.width)
            line.draw()

            # 绘制可派遣载具
            info_draw_2 = draw.NormalDraw()
            info_draw_2.text = _("\n可派遣载具：\n\n")
            info_draw_2.width = self.width
            info_draw_2.draw()

            for vehicle_cid in cache.rhodes_island.vehicles:
                # 如果没有可以派遣的载具，则不绘制
                vehicle_count = cache.rhodes_island.vehicles[vehicle_cid][0] - cache.rhodes_island.vehicles[vehicle_cid][1]
                if vehicle_count <= 0:
                    continue
                vehicle_data = game_config.config_vehicle[vehicle_cid]
                vehicle_speed = str(vehicle_data.speed)
                vehicle_capacity = str(vehicle_data.capacity)
                vehicle_special = vehicle_data.special
                now_choice_count = 0
                if vehicle_cid in self.send_vehicle_dict:
                    now_choice_count = self.send_vehicle_dict[vehicle_cid]

                draw_text = _("[{0}] {1} 当前选择/可选择：{2}/{3} 速度：{4} 运载量：{5} 特殊效果：{6}\n").format(str(vehicle_cid).rjust(2,'0'), vehicle_data.name, now_choice_count, vehicle_count, vehicle_speed, vehicle_capacity, vehicle_special)
                info_draw = draw.NormalDraw()
                info_draw.text = draw_text
                info_draw.width = self.width
                info_draw.draw()

                # 增加一辆
                button_draw = draw.CenterButton(
                    _("[增加一辆]"),
                    f"\n{vehicle_cid}+1",
                    self.width / 6,
                    cmd_func=self.add_this_vehicle,
                    args=vehicle_cid,
                )
                button_draw.draw()
                return_list.append(button_draw.return_text)

                # 减少一辆
                button_draw = draw.CenterButton(
                    _("[减少一辆]"),
                    f"\n{vehicle_cid}-1",
                    self.width / 6,
                    cmd_func=self.reduce_this_vehicle,
                    args=vehicle_cid,
                )
                button_draw.draw()
                return_list.append(button_draw.return_text)

                line_feed.draw()

            now_capacity = 0 # 当前运载量
            now_speed = 99 # 当前速度
            now_effect = [] # 当前效果

            # 遍历已选择的载具
            for vehicle_id in self.send_vehicle_dict:
                vehicle_data = game_config.config_vehicle[vehicle_id]
                now_capacity += vehicle_data.capacity * self.send_vehicle_dict[vehicle_id]
                now_speed = min(now_speed, vehicle_data.speed)
                if vehicle_data.special != "无" and vehicle_data.special not in now_effect:
                    now_effect.append(vehicle_data.special)
            if now_speed == 99:
                now_speed = 1

            # 遍历效果，输出效果文本
            effect_text = ""
            for effect in now_effect:
                effect_text += f"{effect} "

            # 绘制当前载具的总信息
            info_draw = draw.NormalDraw()
            info_draw_text = _("\n")
            info_draw_text += _("当前总运载量/需要运载量：{0}/{1}\n").format(now_capacity, commision_capacity_int)
            info_draw_text += _("当前速度（取决于所有载具中最慢的）（未实装）：{0}\n").format(now_speed)
            info_draw_text += _("其他效果（未实装）：{0}\n").format(effect_text)
            info_draw.text = info_draw_text
            info_draw.width = self.width
            info_draw.draw()

            line_feed.draw()
            line_feed.draw()
            back_draw = draw.CenterButton(_("[返回]"), _("返回"), window_width)
            back_draw.draw()
            return_list.append(back_draw.return_text)
            yrn = flow_handle.askfor_all(return_list)
            if yrn == back_draw.return_text:
                break

    def select_this_npc(self, character_id: int):
        """
        选择当前人物
        Keyword arguments:
        character_id -- 人物id
        """
        if character_id in self.send_npc_list:
            self.send_npc_list.remove(character_id)
        else:
            self.send_npc_list.append(character_id)

    def add_this_vehicle(self, vehicle_id: int):
        """
        增加一辆载具
        Keyword arguments:
        vehicle_id -- 载具id
        """
        if vehicle_id not in self.send_vehicle_dict:
            self.send_vehicle_dict[vehicle_id] = 1
        else:
            self.send_vehicle_dict[vehicle_id] += 1
        # 最大不会超过可派遣数量
        vehicle_count = cache.rhodes_island.vehicles[vehicle_id][0] - cache.rhodes_island.vehicles[vehicle_id][1]
        if self.send_vehicle_dict[vehicle_id] > vehicle_count:
            self.send_vehicle_dict[vehicle_id] = vehicle_count

    def reduce_this_vehicle(self, vehicle_id: int):
        """
        减少一辆载具
        Keyword arguments:
        vehicle_id -- 载具id
        """
        if vehicle_id in self.send_vehicle_dict:
            self.send_vehicle_dict[vehicle_id] -= 1
            if self.send_vehicle_dict[vehicle_id] <= 0:
                self.send_vehicle_dict.pop(vehicle_id)

    def send_commision(self, commision_id: int):
        """
        派遣委托
        Keyword arguments:
        commision_id -- 委托编号
        """
        commision_data = game_config.config_commission[commision_id]
        commision_people = commision_data.people
        if len(self.send_npc_list) < commision_people:
            return

        # 绘制委托信息
        draw_text = ""
        draw_text += _("\n\n已派遣")
        for character_id in self.send_npc_list:
            character_data = cache.character_data[character_id]
            character_name = character_data.name
            draw_text += f"{character_name} "
        draw_text += _("执行委托：")
        commision_name = commision_data.name
        draw_text += commision_name
        draw_text += _("，耗时：")
        commision_time = int(commision_data.time)
        draw_text += str(commision_time)
        draw_text += _("天，将在 ")
        new_time = game_time.get_sub_date(day=commision_time)
        new_time_text = game_time.get_date_until_day(new_time)
        draw_text += new_time_text
        draw_text += _(" 返回\n\n")
        info_draw = draw.WaitDraw()
        info_draw.text = draw_text
        info_draw.style = "gold_enrod"
        info_draw.width = window_width
        info_draw.draw()

        # 添加到进行中的委托
        cache.rhodes_island.ongoing_field_commissions[commision_id] = [self.send_npc_list, new_time, []]
        # 消耗资源
        get_commission_demand_and_reward(commision_id, self.send_npc_list, False, True)
        # 遍历派遣人员，设为派遣状态，并离线
        for character_id in self.send_npc_list:
            cache.character_data[character_id].sp_flag.field_commission = commision_id
            default.handle_chara_off_line(character_id, 1, change_data = game_type.CharacterStatusChange, now_time = cache.game_time)
        # 结算派遣的载具
        now_vehicle_list = []
        for vehicle_id in self.send_vehicle_dict:
            cache.rhodes_island.vehicles[vehicle_id][1] += self.send_vehicle_dict[vehicle_id]
            for i in range(self.send_vehicle_dict[vehicle_id]):
                now_vehicle_list.append(vehicle_id)
        cache.rhodes_island.ongoing_field_commissions[commision_id][2] = now_vehicle_list
        # 清空派遣人员与载具
        self.send_npc_list = []
        self.send_vehicle_dict = {}
