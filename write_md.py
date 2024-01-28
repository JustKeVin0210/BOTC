import pandas as pd
import json
import math
import os


def read_data(file_dir):
    data_frame = pd.read_excel(file_dir, sheet_name="全角色")
    return data_frame


def write_md(file_dir, json_dir, output_dir):
    data_frame = read_data(file_dir)
    with open(json_dir, "r", encoding='utf-8') as f:
        script_roles = json.load(f)
    script_roles_fisrt_night = sorted([i for i in script_roles if i.get("firstNight")],
                                      key=lambda x: x.get("firstNight"))
    script_roles_other_night = sorted([i for i in script_roles if i.get("otherNight")],
                                      key=lambda x: x.get("otherNight"))
    # print("首夜\n", [i.get('name') for i in script_roles_fisrt_night])
    # print("其他夜\n", [i.get('name') for i in script_roles_other_night])
    with open(output_dir, "w") as f:
        f.write("| 角色图标 | 角色名 | 角色类型 | 剧本 | 首夜行动顺序 | 角色图标 | 角色名 | 角色类型 | 剧本 | 其他夜行动顺序 |\n")
        f.write("|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|\n")
        for line in data_frame.values:
            first_role = line[0:4]
            other_role = line[4:8]
            if math.isnan(first_role[-1]):
                f.write("| | | | | |")
            else:
                for i, role in enumerate(script_roles_fisrt_night):
                    if role.get("firstNight") == first_role[-1] and role.get("name") == first_role[0]:
                        f.write("| <img src=\"{}\" width=\"50%\"> | {} | {} | {} | {} |".format(
                            role.get("image"), first_role[0], first_role[1], first_role[2], int(first_role[3])))
                        script_roles_fisrt_night.pop(i)
            for i, role in enumerate(script_roles_other_night):
                if role.get("otherNight") == other_role[-1] and role.get("name") == other_role[0]:
                    f.write(" <img src=\"{}\" width=\"50%\"> | {} | {} | {} | {} |\n".format(
                        role.get("image"), other_role[0], other_role[1], other_role[2], int(other_role[3])))
                    script_roles_other_night.pop(i)
            # print(line)
    return


if __name__ == '__main__':
    file_dir = r"./角色行动顺序表-20240126更新版.xlsx"
    json_dir = r"./全角色.json"
    output_dir = r"./角色行动顺序表.md"
    write_md(file_dir, json_dir, output_dir)
