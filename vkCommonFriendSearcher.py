import requests
import time
from collections import deque

VK_VERSION = '5.101'

def get_friends_request_url(user_id, access_token):
    return 'https://api.vk.com/method/friends.get?user_id=' + str(user_id) + '&fields=name&access_token=' + access_token + '&v=' + VK_VERSION


def get_user_id_from_domain(domain, access_token):
    url = 'https://api.vk.com/method/users.get?user_ids=' + domain + '&access_token=' + access_token + '&v=' + VK_VERSION
    responce = requests.get(url)
    json_responce = responce.json()
    return json_responce['response'][0]['id']

def get_user_name(user_id):
    user_id = str(user_id)
    url = 'https://api.vk.com/method/users.get?user_ids=' + user_id + '&access_token=' + access_token + '&v=' + VK_VERSION
    responce = requests.get(url)
    json_responce = responce.json()
    return json_responce['response'][0]['first_name'] + ' ' + json_responce['response'][0]['last_name']


def getdata():
    f = open("input.txt", "r")
    access_token = f.readline().rstrip()
    domain1 = f.readline().rstrip()
    domain2 = f.readline().rstrip()
    return access_token, get_user_id_from_domain(domain1, access_token), get_user_id_from_domain(domain2, access_token)

def get_way(parents, user_id):
    if user_id == -1:
        return list()

    tmp_list = get_way(parents, parents[user_id])
    tmp_list.append(get_user_name(user_id))
    return tmp_list


def app_run(access_token, user_id1, user_id2):
    parents = {user_id1 : -1}
    queue = deque([user_id1])

    while(True):
        try:
            current_user = queue.popleft()

            friends_url = get_friends_request_url(current_user, access_token)
            responce = requests.get(friends_url)
            json_responce = responce.json()
            friends_list = json_responce['response']['items']
            friends_ids = []

            for i in friends_list:
                friends_ids.append(i['id'])

            for friend in friends_ids:
                if friend not in parents:
                    parents[friend] = current_user
                    queue.append(friend)
                if friend == user_id2:
                    return get_way(parents, user_id2)
        except:
            print(json_responce)
            
        time.sleep(1)

    return 'No way :('

access_token, user_id1, user_id2 = getdata()
print('Your way is:\n', app_run(access_token, user_id1, user_id2))
