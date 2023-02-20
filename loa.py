import requests
from datetime import datetime
import telegram
import asyncio

async def send_telegram(result):
    bot = telegram.Bot(token="6182942706:AAGOeTFNNikciG1dA0TPPSUcG4w9lIIlml8")
    chat_id = "5199414164"
    await bot.send_message(chat_id=chat_id, text=result)

def card_pick():
    # Return a list of cards to monitor
    return ["에버그레이스 카드", "웨이 카드", "바르칸 카드", 
            "어린 아만 카드", "라자람 카드", "라카이서스 카드", "베히모스 카드", "세헤라데 카드", "칼테이야 카드", "파이어혼 카드",
            "클라우디아 카드", "마레가 카드", "마리우 카드", "아이작 카드", "칼리나리 네리아 카드", 
            "베라드 카드", "닐라이 카드"]

def server_pick(server_name):
    # Return the server number based on the server name
    if server_name == "카단":
        return "5"
    else:
        raise ValueError("Unsupported server name")

def call_api(server_number, cards):
    url = f"https://api.korlark.com/merchants?limit=15&server={server_number}"
    headers = {"X-Requested-With": "XMLHttpRequest"}
    response = requests.get(url, headers=headers, verify=True)
    data = response.json()

    now = datetime.utcnow()
    card_list = ""

    for p in cards:
        for c in data["merchants"]:
            if c["card"] == p:
                created_time = int(c["created_at"][-8:-6])
                if created_time == now.hour:
                    card_list += f"{p} {c['continent']} {c['zone']} {c['created_at']}\n"
                    print(card_list)

    return card_list

def main():
    try:
        pick_server_name = "카단"
        pick_cards = card_pick()
        server_number = server_pick(pick_server_name)
        result = call_api(server_number, pick_cards)

        if result:
            asyncio.run(send_telegram(result))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
