import random
import datetime
from Script.Core import (
    cache_control,
    value_handle,
    game_type,
)
from Script.Design import game_time
from Script.Config import game_config

cache: game_type.Cache = cache_control.cache
""" 游戏内缓存数据 """


def get_Favorability_zero() -> dict:
    """
    直接将初始好感归为{0:0}
    """
    return {0:0}

def get_Trust_zero() -> dict:
    """
    直接将初始信赖归为0
    """
    return 0

def get_ability_zero(ability_dict) -> dict:
    """
    检查初始能力，将为空的项补为0
    """
    ability_list = ability_dict
    for ability in game_config.config_ability:
        if ability not in ability_dict:
            ability_list[ability] = 0
    return ability_list

def get_experience_zero(experience_dict) -> dict:
    """
    检查初始经验，将为空的项补为0
    """
    experience_list = experience_dict
    for experience in game_config.config_experience:
        if experience not in experience_dict:
            experience_list[experience] = 0
    return experience_list

def get_juel_zero(juel_dict) -> dict:
    """
    检查初始宝珠，将为空的项补为0
    """
    juel_list = juel_dict
    for juel in game_config.config_juel:
        if juel not in juel_dict:
            juel_list[juel] = 0
    return juel_list

def get_Dr_talent_zero(juel_dict) -> dict:
    """
    检查是否是0号角色，将特定项补为0
    """
    juel_list = juel_dict
    juel_list[4] = 1
    juel_list[5] = 1
    return juel_list


def get_rand_npc_birthday(age: int):
    """
    随机生成npc生日
    Keyword arguments:
    age -- 年龄
    """
    now_year = cache.game_time.year
    now_month = cache.game_time.month
    now_day = cache.game_time.day
    birth_year = now_year - int(age)
    birthday = game_time.get_rand_day_for_year(birth_year)
    if now_month < birthday.month or (now_month == birthday.month and now_day < birthday.day):
        birthday = game_time.get_sub_date(year=-1, old_date=birthday)
    return birthday


def get_max_hit_point(tem_id: int) -> int:
    """
    获取最大hp值
    Keyword arguments:
    tem_id -- hp模板id
    Return arguments:
    int -- 最大hp值
    """
    tem_data = game_config.config_hitpoint_tem[tem_id]
    max_hit_point = tem_data.max_value
    add_value = value_handle.get_gauss_rand(0, 500)
    impairment = value_handle.get_gauss_rand(0, 500)
    return max_hit_point + add_value - impairment


def get_max_mana_point(tem_id: int) -> int:
    """
    获取最大mp值
    Keyword arguments:
    tem_id -- mp模板
    Return arguments:
    int -- 最大mp值
    """
    tem_data = game_config.config_manapoint_tem[tem_id]
    max_mana_point = tem_data.max_value
    add_value = value_handle.get_gauss_rand(0, 500)
    impairment = value_handle.get_gauss_rand(0, 500)
    return max_mana_point + add_value - impairment


def get_experience_level_weight(experience: int) -> int:
    """
    按经验计算技能等级权重
    Keyword arguments:
    experience -- 经验数值
    Return arguments:
    int -- 权重
    """
    grade = 0
    if experience < 100:
        grade = 0
    elif experience < 500:
        grade = 1
    elif experience < 1000:
        grade = 2
    elif experience < 2000:
        grade = 3
    elif experience < 3000:
        grade = 4
    elif experience < 5000:
        grade = 5
    elif experience < 10000:
        grade = 6
    elif experience < 20000:
        grade = 7
    elif experience >= 20000:
        grade = 8
    return grade


def judge_grade(experience: int) -> str:
    """
    按经验数值评定等级
    Keyword arguments:
    experience -- 经验数值
    Return arguments:
    str -- 评级
    """
    grade = ""
    if experience < 100:
        grade = "G"
    elif experience < 500:
        grade = "F"
    elif experience < 1000:
        grade = "E"
    elif experience < 2000:
        grade = "D"
    elif experience < 3000:
        grade = "C"
    elif experience < 5000:
        grade = "B"
    elif experience < 10000:
        grade = "A"
    elif experience < 20000:
        grade = "S"
    elif experience >= 20000:
        grade = "EX"
    return grade

def get_status_level(value: int) -> int:
    """
    按状态数值评定数字等级
    Keyword arguments:
    value -- 属性数值
    Return arguments:
    level -- 数字评级
    """
    if value < 100:
        level = 0
    elif value < 500:
        level = 1
    elif value < 3000:
        level = 2
    elif value < 10000:
        level = 3
    elif value < 30000:
        level = 4
    elif value < 60000:
        level = 5
    elif value < 100000:
        level = 6
    elif value < 150000:
        level = 7
    elif value < 250000:
        level = 8
    elif value < 400000:
        level = 9
    elif value >= 400000:
        level = 10
    return level


def get_ability_level(value: int) -> int:
    """
    按能力数值评定数字等级
    Keyword arguments:
    value -- 能力数值
    Return arguments:
    level -- 数字评级
    """
    if value < 100:
        level = 0
    elif value < 500:
        level = 1
    elif value < 3000:
        level = 2
    elif value < 10000:
        level = 3
    elif value < 30000:
        level = 4
    elif value < 60000:
        level = 5
    elif value < 100000:
        level = 6
    elif value < 150000:
        level = 7
    elif value < 250000:
        level = 8
    elif value < 400000:
        level = 9
    elif value >= 400000:
        level = 10
    return level

def get_ability_adjust(value: int) -> int:
    """
    按能力数值评定修正比例
    Keyword arguments:
    value -- 能力数值
    Return arguments:
    just -- 调整比例
    """
    level = get_ability_level(value)
    if level == 0:
        just = 0.2
    elif level == 1:
        just = 0.4
    elif level == 2:
        just = 0.7
    elif level == 3:
        just = 1.0
    elif level == 4:
        just = 1.4
    elif level == 5:
        just = 1.8
    elif level == 6:
        just = 2.3
    elif level == 7:
        just = 2.8
    elif level == 8:
        just = 3.4
    elif level == 9:
        just = 4.0
    elif level == 10:
        just = 5.0
    return just

