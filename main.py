import time
import requests
import random

with open('addresses.txt', 'r') as file:
    addresses = file.readlines()

with open('proxies.txt', 'r') as file:
    proxies = file.readlines()


def get_user_agent():
    random_version = f"{random.uniform(520, 540):.2f}"
    return (f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random_version} (KHTML, like Gecko)'
            f' Chrome/126.0.0.0 Safari/{random_version} Edg/126.0.0.0')


def info(address, proxy):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9,ru-RU;q=0.8,zh-TW;q=0.7,zh;q=0.6',
        'origin': 'https://scrollpump.xyz',
        'priority': 'u=1, i',
        'referer': 'https://scrollpump.xyz/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': get_user_agent()
    }

    params = {
        'address': address,
    }

    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }
    
    response = requests.get('https://api.scrollpump.xyz/api/Airdrop/GetReward', params=params, headers=headers, proxies=proxies)
    
    count_token = 0
    
    if response.status_code == 200:
        data = response.json()
        if data['data']['baseReward']:
            count_token += data['data']['baseReward']
        if data['data']['bonusReward']:
            count_token += data['data']['bonusReward']

    return count_token


if __name__ == "__main__":
    total_token = 0
    
    for index, address in enumerate(addresses):
        
        address = address.strip()
        count_token = info(address.lower(), proxies[index])
        print(f'{address}:{count_token}')
        
        total_token += count_token
        time.sleep(1)

    print(f"Общее количество токенов PUMP: {total_token}")
