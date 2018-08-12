import requests

CURRENT_YEAR = 2018
VK_API_VERSION = 5.71
ACCESS_TOKEN = \
    ('17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711')


def fetch_user_id(uid):
    params = {
        'v': VK_API_VERSION,
        'access_token': ACCESS_TOKEN,
        'user_ids': uid,
    }
    res_users_get = requests.get('https://api.vk.com/method/users.get', params)
    user_id = res_users_get.json()['response'][0]['id']
    return user_id


def fetch_user_friends(user_id):
    params = {
        'v': VK_API_VERSION,
        'access_token': ACCESS_TOKEN,
        'user_id': user_id,
        'fields': 'bdate',
    }
    res_friends = requests.get('https://api.vk.com/method/friends.get', params)
    friends = res_friends.json()['response']['items']
    return friends


def group_friends_ages(friends):
    counter_ages = {}
    for friend in friends:
        bdate = friend.get('bdate')
        if not bdate:
            continue
        split_bdate = bdate.split('.')
        if len(split_bdate) != 3:
            continue
        day, month, year = split_bdate
        age = CURRENT_YEAR - int(year)
        counter_ages.setdefault(age, 0)
        counter_ages[age] += 1
    group_by_ages = list(counter_ages.items())
    group_by_ages.sort(key=lambda x: (-x[1], x[0]))
    return group_by_ages


def calc_age(uid):
    user_id = fetch_user_id(uid)
    friends = fetch_user_friends(user_id)
    group_ages = group_friends_ages(friends)
    return group_ages


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
