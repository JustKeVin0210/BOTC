import os
import time
import requests
import json
from bs4 import BeautifulSoup
from bisect import bisect_left


URL = "https://clocktower-wiki.gstonegames.com/index.php?title=%E7%9B%B8%E5%85%8B%E8%A7%84%E5%88%99"


def crawl_info(jinx_url=URL):
    response = requests.get(jinx_url)
    response.encoding = "utf-8"
    html_txt = BeautifulSoup(response.text, "html.parser")
    html_find_all = html_txt.find_all("p")
    jinx_role_list = []
    jinx_ability_list = []
    for html_find in html_find_all[1:]:
        jinx_roles = []
        for html_a in html_find.find_all("a"):
            jinx_roles.append(html_a.get('title'))
        if len(jinx_roles) != 2:
            for role1, role2 in zip(jinx_roles[0:1] * (len(jinx_roles) - 1), jinx_roles[1:]):
                jinx_role_list.append([role1, role2])
                jinx_ability_list.append(jinx_ability)
            continue
        jinx_role_list.append(jinx_roles)
        jinx_ability = html_find.contents[-1][1:-1]
        jinx_ability_list.append(jinx_ability)
    return jinx_role_list, jinx_ability_list


def get_role_info(role_file):
    with open(role_file, "r", encoding='utf-8') as f:
        role_info_list = json.load(f)
    if role_info_list[0].get("id") == "_meta":
        role_info_list.pop(0)
    role_info = sorted(role_info_list, key=lambda x: x.get("name"))
    return role_info


def download_jinx(role_file, save_file):
    jinx_dict_list = [
        {
            "id": "_meta",
            "name": "相克规则",
            "author": "Just_KeVin",
            "logo": "https://github.com/JustKeVin0210/BOTC/blob/main/image/get_ability/Marionette/change_team/townsfolk/Marionette_Atheist.png?raw=true",
            "ability_jinx": "相克规则",
            "ability_role": "衍生角色"
        }
    ]
    role_info = get_role_info(role_file)
    jinx_role_list, jinx_ability_list = crawl_info(jinx_url=URL)
    for (jinx_role_1, jinx_role_2), jinx_ability in zip(jinx_role_list, jinx_ability_list):
        jinx_dict = {}
        index_1 = bisect_left(role_info, jinx_role_1, key=lambda x: x.get("name"))
        index_2 = bisect_left(role_info, jinx_role_2, key=lambda x: x.get("name"))

        jinx_dict["id"] = role_info[index_1].get("id").replace("TRANS", "") + "+" + role_info[index_2].get("id").replace("TRANS", "")
        jinx_dict["image"] = f"https://github.com/JustKeVin0210/BOTC/blob/main/image/jinx/{jinx_dict['id'].replace('+', '_')}.png?raw=true"
        jinx_dict["edition"] = "custom"
        jinx_dict["team"] = "ability_jinx"
        jinx_dict["name"] = role_info[index_1].get("name") + "&" + role_info[index_2].get("name")
        jinx_dict["ability"] = jinx_ability
        jinx_dict_list.append(jinx_dict)
    # 将数据写入json文件
    with open(save_file, "w", encoding='utf-8') as f:
        json.dump(jinx_dict_list, f, ensure_ascii=False, indent=2)
    print(f"冲突规则已经保存到{os.path.basename(save_file)}")
    return


if __name__ == '__main__':
    role_file = r"./全角色.json"
    save_file = r"./冲突规则.json"
    download_jinx(role_file, save_file)
