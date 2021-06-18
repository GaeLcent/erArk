class Ability:
    """ 能力对应类型和文字描述 """

    cid: int
    """ 能力id """
    ability_type: int
    """ 类型(0:感觉,1:扩张,2:刻印,3:基础) """
    name: str
    """ 名字 """


class AbilityType:
    """ 角色能力类型 """

    cid: int
    """ 类型id """
    name: str
    """ 类型名 """


class BarConfig:
    """ 比例条名字对应的状态图片和绘制宽度 """

    cid: int
    """ 比例条id """
    name: str
    """ 比例条名字 """
    ture_bar: str
    """ 进度条图片 """
    null_bar: str
    """ 背景条图片 """
    width: int
    """ 图片绘制宽度 """


class BehaviorEffect:
    """ 行为结算器配置 """

    cid: int
    """ 表id """
    behavior_id: int
    """ 行为id """
    effect_id: int
    """ 结算器id """


class Book:
    """ 书籍配置表 """

    cid: int
    """ 书本id """
    name: str
    """ 名字 """
    info: str
    """ 介绍 """


class CharacterState:
    """ 角色状态属性表 """

    cid: int
    """ 配表id """
    name: str
    """ 状态名字 """
    type: int
    """ 状态类型 """


class CharacterStateType:
    """ 角色状态类型 """

    cid: int
    """ 类型id """
    name: str
    """ 类型名 """


class ClothingEvaluate:
    """ 服装评价描述 """

    cid: int
    """ 评价id """
    name: str
    """ 评价名 """


class ClothingSuit:
    """ 套装配置数据 """

    cid: int
    """ 套装id """
    clothing_id: int
    """ 服装id """
    suit_type: int
    """ 套装编号 """
    sex: int
    """ 性别限制 """


class ClothingTem:
    """ 服装模板 """

    cid: int
    """ 模板id """
    name: str
    """ 服装名字 """
    clothing_type: int
    """ 服装类型 """
    sex: int
    """ 服装性别限制 """
    tag: int
    """ 服装用途标签 """
    describe: str
    """ 描述 """


class ClothingType:
    """ 衣服种类配置 """

    cid: int
    """ 类型id """
    name: str
    """ 类型名字 """


class ClothingUseType:
    """ 服装用途配置 """

    cid: int
    """ 用途id """
    name: str
    """ 用途名字 """


class Course:
    """ 课程配置数据 """

    cid: int
    """ 课程id """
    name: str
    """ 名字 """


class EndAgeTem:
    """ 性别对应平均寿命 """

    cid: int
    """ 模板id """
    sex: int
    """ 性别id """
    end_age: int
    """ 平均寿命 """


class Experience:
    """ 经验名字 """

    cid: int
    """ 经验id """
    name: str
    """ 经验名 """


class FontConfig:
    """ 字体样式配置数据(富文本用) """

    cid: int
    """ 样式id """
    name: str
    """ 字体名 """
    foreground: str
    """ 前景色 """
    background: str
    """ 背景色 """
    font: str
    """ 字体 """
    font_size: int
    """ 字体大小 """
    bold: bool
    """ 加粗 """
    underline: bool
    """ 下划线 """
    italic: bool
    """ 斜体 """
    selectbackground: str
    """ 选中时背景色 """
    info: str
    """ 备注 """


class Food:
    """ 食材配置数据 """

    cid: int
    """ 食材id """
    name: str
    """ 食材名字 """
    cook: bool
    """ 可烹饪 """
    eat: bool
    """ 可食用 """
    seasoning: bool
    """ 可作为调料 """
    fruit: bool
    """ 是水果 """


class FoodFeel:
    """ 食材效果配置数据 """

    cid: int
    """ 表id """
    food_id: int
    """ 所属食材id """
    feel_id: int
    """ 效果id """
    feel_value: float
    """ 效果数值 """


class FoodQualityWeight:
    """ 烹饪技能等级制造食物品质权重配置 """

    cid: int
    """ 配置表id """
    level: int
    """ 烹饪技能等级 """
    quality: int
    """ 食物品质 """
    weight: int
    """ 权重 """


class HitPointTem:
    """ hp模板对应平均值 """

    cid: int
    """ 模板id """
    max_value: int
    """ 最大值 """


class InstructType:
    """ 指令类型配置 """

    cid: int
    """ 指令类型id """
    name: str
    """ 名字 """


class Item:
    """ 道具配置数据 """

    cid: int
    """ 道具id """
    name: str
    """ 道具名 """
    tag: str
    """ 标签 """
    info: str
    """ 描述 """


class Juel:
    """ 珠名字 """

    cid: int
    """ 珠id """
    name: str
    """ 珠名 """


class ManaPointTem:
    """ mp模板对应平均值 """

    cid: int
    """ 模板id """
    max_value: int
    """ 最大值 """


class Moon:
    """ 月相配置(明日更满为正反之为负) """

    cid: int
    """ 月相id """
    name: str
    """ 月相 """
    type: int
    """ 月相类型 """
    min_phase: float
    """ 最小亮度 """
    max_phase: float
    """ 最大亮度 """


class MoveMenuType:
    """ 移动菜单类型 """

    cid: int
    """ 移动类型id """
    name: str
    """ 名字 """


class Nature:
    """ 性格倾向配置 """

    cid: int
    """ 性格id """
    nature_type: int
    """ 类型 """
    good: str
    """ 正面倾向 """
    bad: str
    """ 负面倾向 """


class NatureTag:
    """ 性格倾向标签 """

    cid: int
    """ 性格标签id """
    good: str
    """ 正面倾向 """
    bad: str
    """ 负面倾向 """


class Organ:
    """ 器官对应性别限定和文字描述 """

    cid: int
    """ 器官id """
    organ_type: int
    """ 类型(0:女,1:男,2:通用) """
    name: str
    """ 名字 """


class Profession:
    """ 职业类型名称 """

    cid: int
    """ 职业id """
    name: str
    """ 职业名 """


class Race:
    """ 种族类型名称 """

    cid: int
    """ 种族id """
    name: str
    """ 种族名 """


class Recipes:
    """ 菜谱配置 """

    cid: int
    """ 菜谱id """
    name: str
    """ 菜谱名字 """
    time: int
    """ 烹饪时间 """


class RecipesFormula:
    """ 菜谱配方配置 """

    cid: int
    """ 配方id """
    recipe_id: int
    """ 所属菜谱id """
    formula_type: int
    """ 配方类型 """
    food_id: int
    """ 食材id """


class RecipesFormulaType:
    """ 菜谱配方类型 """

    cid: int
    """ 表id """
    name: str
    """ 菜谱配方名字 """


class School:
    """ 学校配置 """

    cid: int
    """ 学校id """
    name: str
    """ 名字 """
    day: int
    """ 每周上课天数 """
    min_age: int
    """ 最小年龄 """
    max_age: int
    """ 最大年龄 """


class SchoolPhaseCourse:
    """ 各学校各年级教学科目配置 """

    cid: int
    """ 配表id """
    school: int
    """ 学校id """
    phase: int
    """ 年级 """
    course: int
    """ 课程id """


class SchoolSession:
    """ 各学校上课时间配置 """

    cid: int
    """ 配表id """
    school_id: int
    """ 学校id """
    session: int
    """ 当天课时编号 """
    start_time: int
    """ 开始时间 """
    end_time: int
    """ 结束时间 """


class Season:
    """ 季节配置 """

    cid: int
    """ 季节id """
    name: str
    """ 季节名 """


class SexTem:
    """ 性别对应描述和性别器官模板 """

    cid: int
    """ 性别id """
    name: str
    """ 性别名称 """
    has_man_organ: bool
    """ 是否有男性器官 """
    has_woman_organ: bool
    """ 是否有女性器官 """
    region: int
    """ 随机npc生成性别权重 """


class SocialType:
    """ 关系类型配置 """

    cid: int
    """ 关系id """
    name: str
    """ 名字 """


class SolarPeriod:
    """ 节气配置 """

    cid: int
    """ 节气id """
    name: str
    """ 节气名 """
    season: int
    """ 所属季节id """


class Status:
    """ 状态描述配置 """

    cid: int
    """ 状态id """
    name: str
    """ 描述 """


class SunTime:
    """ 太阳时间配置 """

    cid: int
    """ 太阳时间id """
    name: str
    """ 太阳时间名 """


class Talent:
    """ 素质对应类型和文字描述 """

    cid: int
    """ 素质id """
    Talent_type: int
    """ 类型(0:性素质,1:身体素质,2:精神素质,3:技术素质,4:其他素质) """
    name: str
    """ 名字 """
    info: str
    """ 备注说明 """


class TalentType:
    """ 角色能力类型 """

    cid: int
    """ 类型id """
    name: str
    """ 类型名 """


class WeekDay:
    """ 星期描述配置 """

    cid: int
    """ 周id """
    name: str
    """ 描述 """


class TalkPremise:
    """ 口上前提表 """

    cid: str
    """ 配表id """
    talk_id: str
    """ 所属口上id """
    premise: str
    """ 前提id """


class Talk:
    """ 口上配置数据 """

    cid: str
    """ 口上id """
    behavior_id: int
    """ 触发口上的行为id """
    adv_id: int
    """ 口上限定的剧情npcid """
    context: str
    """ 口上内容 """


































































































class TargetEffect:
    """ 执行目标所能达成的效果id """

    cid: str
    """ 配表id """
    target_id: str
    """ 所属目标id """
    effect_id: str
    """ 达成的效果id（即达成的前提id） """


class TargetPremise:
    """ 执行目标所需的前提id """

    cid: str
    """ 配表id """
    target_id: str
    """ 所属目标id """
    premise_id: str
    """ 所需前提id """


class Target:
    """ ai的目标 """

    cid: str
    """ 目标id """
    state_machine_id: int
    """ 执行的状态机id """
    remarks: str
    """ 备注 """
