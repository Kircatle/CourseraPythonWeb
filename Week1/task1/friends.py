"""
Клиент к API VK, который считает распределение возрастов друзей для указанного
пользователя. То есть на вход подается username или user_id пользователя, на
выходе получаем список пар (<возраст>, <количество друзей с таким возрастом>),
отсортированный по убыванию по второму ключу (количество друзей) и по
возрастанию по первому ключу (возраст).
"""
import requests
import json
import datetime


def distribution_age(friends_age):
    dist = dict()
    for friends in friends_age:
        dist.setdefault(friends, 0)
        dist[friends] += 1
    return sorted(dist.items(), key=lambda x: (-x[1], x[0]))


def get_age_via_date(friends_date):
    list_age = list()
    now_year = int(datetime.datetime.now().year)
    for year in friends_date:
        year = year.split(".")
        if len(year) < 3:
            continue
        age = now_year-int(year[2])
        list_age.append(age)
    return list_age


def get_date_friends(uid, token):
    friends_date = list()
    url_api_get_friends = "https://api.vk.com/method/friends.get"
    params_get_friends = {
            "user_id": uid,
            "access_token": token,
            "v": "5.71",
            "fields": "bdate",
            }
    friends = requests.get(url_api_get_friends, params_get_friends).text
    friends = json.loads(friends)["response"]["items"]
    for human in friends:
        friends_date.append(human.setdefault("bdate", ""))
    return friends_date


def get_uid(uid, token):
    url_api_get_user = "https://api.vk.com/method/users.get"
    params_get_user = {
             "user_ids": uid,
             "access_token": token,
             "v": "5.71"
            }
    uid = requests.get(url_api_get_user, params_get_user).text
    uid = json.loads(uid)["response"][0]['id']
    return uid


def calc_age(uid):
    token = (
        "2f2dbe8f2f2dbe8f2f2dbe8f2d2f5e85c2" +
        "22f2d2f2dbe8f700db2ff72744651740f3e0e"
            )
    uid = get_uid(uid, token)
    friends_date = get_date_friends(uid, token)
    friends_age = get_age_via_date(friends_date)
    dist = distribution_age(friends_age)
    return dist


if __name__ == "__main__":
    age = calc_age("id189128094")
    print(age)
