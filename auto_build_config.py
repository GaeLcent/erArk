import csv
import os
import json
import datetime
import ast
import time


config_dir = os.path.join("data", "csv")
event_dir = os.path.join("data", "event")
talk_dir = os.path.join("data", "talk")
target_dir = os.path.join("data", "target")
config_data = {}
config_def_str = ""
msgData = set()
class_data = set()
character_dir = os.path.join("data", "character")
character_data = {}
ui_text_dir = os.path.join("data", "ui_text")
ui_text_data = {}
po_csv_path = os.path.join("data", "po", "zh_CN", "LC_MESSAGES", "erArk_csv.po")
po_talk_path = os.path.join("data", "po", "zh_CN", "LC_MESSAGES", "erArk_talk.po")
config_po, talk_po = "", ""
built = []

def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper


def build_csv_config(file_path: str, file_name: str, talk: bool, target: bool):
    global config_data, config_def_str, msgData, class_data, character_data, ui_text_data, config_po, talk_po, built

    with open(file_path, encoding="utf-8") as now_file:
        now_read = csv.DictReader(now_file)
        now_docstring_data = {}
        now_type_data = {}
        get_text_data = {}
        file_id = file_name.split(".")[0]
        
        if talk or target:
            path_list = file_path.split(os.sep)
            if talk:
                file_id = path_list[-2] + "_" + file_id
        
        i = 0
        class_text = ""
        type_text = file_id
        
        if talk:
            type_text = "Talk"
            if "premise" in file_name:
                type_text = "TalkPremise"
        elif target:
            if "target" in file_name:
                type_text = "Target"
            elif "premise" in file_name:
                type_text = "TargetPremise"
            elif "effect" in file_name:
                type_text = "TargetEffect"
        
        config_data.setdefault(type_text, {})
        config_data[type_text].setdefault("data", [])
        config_data[type_text].setdefault("gettext", {})

        rows = list(now_read)  # Read all rows at once to avoid multiple file reads

        for j, row in enumerate(rows):
            # Get the current line number
            now_index = j + 2  # CSV reader starts counting from 1, so add 1 more for header lines
            if not i:
                now_docstring_data.update(row)
                i += 1
                continue
            elif i == 1:
                now_type_data.update(row)
                i += 1
                continue
            elif i == 2:
                get_text_data.update({k: int(v) for k, v in row.items()})
                i += 1
                continue
            elif i == 3:
                class_text = list(row.values())[0]
                i += 1
                continue
            
            processed_row = {}
            for k, val in row.items():
                if not val:
                    continue
                now_type = now_type_data[k]
                if now_type == "int":
                    processed_row[k] = int(val)
                elif now_type == "str":
                    processed_row[k] = str(val).replace('"', '\\"')  # Escape quotes to prevent issues in po files
                elif now_type == "bool":
                    processed_row[k] = int(val)
                elif now_type == "float":
                    processed_row[k] = float(val)
                
                if k == "cid" and talk:
                    processed_row[k] = file_id + val
                if k == "talk_id" and talk:
                    processed_row[k] = file_id.split("-")[0] + val
                if k == "cid" and target:
                    processed_row[k] = path_list[-2] + val
                elif k == "target_id" and target:
                    processed_row[k] = path_list[-2] + val
                
                if get_text_data.get(k):
                    build_config_po(val, file_path, now_index, talk)
            
            config_data[type_text]["data"].append(processed_row)
        
        config_data[type_text]["gettext"] = get_text_data
        build_config_def(type_text, now_type_data, now_docstring_data, class_text)


def build_config_def(class_name: str, value_type: dict, docstring: dict, class_text: str):
    global config_def_str, class_data
    if class_name not in class_data:
        # 给talk补上一个头部空行
        if class_name == "Talk":
            config_def_str += "\n\n"
        config_def_str += f"class {class_name}:"
        config_def_str += f'\n    """{class_text}"""\n'
        for k, v in value_type.items():
            config_def_str += f"\n    {k}: {v}"
            config_def_str += f'\n    """{docstring[k]}"""'
        class_data.add(class_name)
    # 去掉因为talk的csv文件而多出的尾部空行
    else:
        while config_def_str.endswith('\n'):
            config_def_str = config_def_str[:-1]
        if config_def_str.endswith('\n'):
            config_def_str = config_def_str[:-1]


def build_config_po(message: str, file_path: str, now_index: int, talk: bool = False):
    global config_po, talk_po, built
    if message not in built:
        po_entry = f'#: .\\{file_path}:{now_index}\nmsgid "{message}"\nmsgstr ""\n\n'
        if talk:
            talk_po += po_entry
        else:
            config_po += po_entry
        built.append(message)


def build_scene_config(data_path):
    global config_po
    for i in os.listdir(data_path):
        now_path = os.path.join(data_path, i)
        if os.path.isfile(now_path):
            if i == "Scene.json":
                with open(now_path, "r", encoding="utf-8") as now_file:
                    scene_data = json.loads(now_file.read())
                    scene_name = scene_data["SceneName"]
                    if not scene_name in built:
                        config_po += f"#: /'{now_path}:2\n"
                        config_po += f'msgid "{scene_name}"\n'
                        config_po += 'msgstr ""\n\n'
                        built.append(scene_name)
            elif i == "Map.json":
                with open(now_path, "r", encoding="utf-8") as now_file:
                    map_data = json.loads(now_file.read())
                    map_name = map_data["MapName"]
                    if not map_name in built:
                        config_po += f"#: /'{now_path}:2\n"
                        config_po += f'msgid "{map_name}"\n'
                        config_po += 'msgstr ""\n\n'
                        built.append(map_name)
        else:
            build_scene_config(now_path)


def build_character_config(file_path:str,file_name:str):
    global config_po,built
    with open(file_path,encoding="utf-8") as now_file:
        now_read = csv.DictReader(now_file)
        file_id = file_name.split(".")[0]
        now_data = {}
        # now_type_data = {}
        i = 0
        for row in now_read:
            # 获得当前的行数
            now_index = now_read.line_num
            if not i:
                i += 1
                continue
            i += 1
            if row["type"] == 'int':
                now_data[row["key"]] = int(row["value"])
            elif row["type"] == 'str':
                now_data[row["key"]] = str(row["value"])
            elif row["type"] == 'dict':
                now_data[row["key"]] = ast.literal_eval(row["value"])
            else:
                now_data[row["key"]] = row["value"]
            if row["get_text"] and row["type"] == 'str' and not row["value"] in built:
                config_po += f"#: .\{file_path}:{now_index}\n"
                config_po += "msgid" + " " + '"' + row["value"] + '"' + "\n"
                config_po += 'msgstr ""\n\n'
                built.append(row["value"])
        character_data[file_id] = now_data

def build_ui_text(file_path:str,file_name:str):
    global config_po,built
    with open(file_path,encoding="utf-8") as now_file:
        now_read = csv.DictReader(now_file)
        file_id = file_name.split(".")[0]
        now_data = {}
        i = 0
        for row in now_read:
            # 获得当前的行数
            now_index = now_read.line_num
            i += 1
            if i <= 4:
                continue
            # print(f"debug row = {row}")
            now_data[row["cid"]] = row["context"]
            if row["context"] not in msgData and not row["context"] in built:
                config_po += f"#: .\{file_path}:{now_index}\n"
                config_po += "msgid" + " " + '"' + row["context"] + '"' + "\n"
                config_po += 'msgstr ""\n\n'
                built.append(row["context"])
        ui_text_data[file_id] = now_data

def build_po_text(po):
    po = "\n"
    po += '# SOME DESCRIPTIVE TITLE.\n'
    po += '# Copyright (C) YEAR Free Software Foundation, Inc.\n'
    po += '# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.\n'
    po += '#\n'
    po += 'msgid ""\n'
    po += 'msgstr ""\n'
    po += '"Project-Id-Version: PACKAGE VERSION\\n"\n'
    po += '"Report-Msgid-Bugs-To: \\n"\n'
    po += '"POT-Creation-Date: 2024-03-11 08:00+0800\\n"\n'
    po += '"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n'
    po += '"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n'
    po += '"Language-Team: LANGUAGE <LANGUAGE-TEAM-EMAIL@ADDRESS>\\n"\n'
    po += '"Language: zh_CN\\n"\n'
    po += '"MIME-Version: 1.0\\n"\n'
    po += '"Content-Type: text/plain; charset=UTF-8\\n"\n'
    po += '"Content-Transfer-Encoding: 8bit\\n"\n\n'
    return po

print("开始加载游戏数据\n")

config_po = build_po_text(config_po)
talk_po = build_po_text(talk_po)

file_list = os.listdir(config_dir)
index = 0
for i in file_list:
    if i.split(".")[1] != "csv":
        continue
    if index:
        config_def_str += "\n\n\n"
    now_file = os.path.join(config_dir, i)
    build_csv_config(now_file, i, 0, 0)
    index += 1

talk_file_list = os.listdir(talk_dir)
start_time = time.time()
for i in talk_file_list:
    # 跳过ai文件夹
    if i == "ai":
        continue
    now_dir = os.path.join(talk_dir, i)
    for f in os.listdir(now_dir):
        config_def_str += "\n"
        # config_def_str += "\n\n\n"
        now_f = os.path.join(now_dir, f)
        build_csv_config(now_f, f, 1, 0)

end_time = time.time()
total_time = end_time - start_time

print(f"The for loop ran in {total_time:.4f} seconds.")

target_file_list = os.listdir(target_dir)
for i in target_file_list:
    now_dir = os.path.join(target_dir, i)
    for f in os.listdir(now_dir):
        config_def_str += "\n\n\n"
        now_f = os.path.join(now_dir, f)
        build_csv_config(now_f, f, 0, 1)

character_file_list = os.listdir(character_dir)
for i in character_file_list:
    now_path = os.path.join(character_dir,i)
    build_character_config(now_path,i)

ui_text_file_list = os.listdir(ui_text_dir)
for i in ui_text_file_list:
    now_path = os.path.join(ui_text_dir,i)
    build_ui_text(now_path,i)

event_list = []
for root, dirs, files in os.walk(event_dir):
    for file in files:
        # 跳过非json文件
        if file.split(".")[-1] != "json":
            continue
        now_event_path = os.path.join(root, file)
        with open(now_event_path, "r", encoding="utf-8") as event_file:
            now_event_data = json.loads(event_file.read())
            for event_id in now_event_data:
                now_event = now_event_data[event_id]
                event_list.append(now_event)
                now_event_text = now_event["text"]
                if now_event_text not in msgData and not now_event_text in built:
                    config_po += f"#: Event:{event_id}\n"
                    config_po += f'msgid "{now_event_text}"\n'
                    config_po += 'msgstr ""\n\n'
                    built.append(now_event_text)
                    msgData.add(now_event_text)
config_data["Event"] = {}
config_data["Event"]["data"] = event_list
config_data["Event"]["gettext"] = {}
config_data["Event"]["gettext"]["text"] = 1

map_path = os.path.join("data", "map")
build_scene_config(map_path)

# print("处理到Character.json了")
data_path = os.path.join("data","Character.json")
with open(data_path,"w",encoding="utf-8") as character_data_file:
    json.dump(character_data,character_data_file,ensure_ascii=0)

# config_path = os.path.join("Script", "Config", "config_def.py")
# config_def_str += "\n"
# with open(config_path, "w", encoding="utf-8") as config_file:
#     config_file.write(config_def_str)

config_data_path = os.path.join("data", "data.json")
with open(config_data_path, "w", encoding="utf-8") as config_data_file:
    json.dump(config_data, config_data_file, ensure_ascii=0)

ui_text_data_path = os.path.join("data", "ui_text.json")
with open(ui_text_data_path, "w", encoding="utf-8") as ui_text_data_file:
    json.dump(ui_text_data, ui_text_data_file, ensure_ascii=0)

# package_path = os.path.join("package.json")
# with open(package_path, "w", encoding="utf-8") as package_file:
#     now_time = datetime.datetime.now()
#     version = f"{now_time.year}.{now_time.month}.{now_time.day}"
#     version_data = {"version": version}
#     json.dump(version_data, package_file, ensure_ascii=0)


# print(f"debug config_po = {config_po}")
# 将po文件写入po_path
with open(po_csv_path, "w", encoding="utf-8") as po_file:
    po_file.write(config_po)

with open(po_talk_path, "w", encoding="utf-8") as po_file:
    po_file.write(talk_po)

print("加载完毕")
