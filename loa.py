import requests
from datetime import datetime, timedelta
import telegram as tel
import asyncio

async def sendTelegram(result): #텔레그램으로 메시지를 보내는 함수
    bot = tel.Bot(token="6182942706:AAGOeTFNNikciG1dA0TPPSUcG4w9lIIlml8")
    chat_id = 5199414164
    cardList = ""  # 한 번에 모아서 보낼 카드 정보 문자열
    if result:
        for card in result:
            if isinstance(card, str):
                cardList += card + "\n"  # 카드 정보를 한 줄씩 추가
            else:
                cardList += card.get_text() + "\n"  # 카드 정보를 한 줄씩 추가
        await bot.sendMessage(chat_id=chat_id, text=cardList)  # 한 번에 모은 카드 정보를 보냄

def card_pick():  # 호출 원하는 카드 목록 불러오는 함수, 우선은 하드코딩으로 목록화해두자
    pick = ["에버그레이스 카드", "웨이 카드", "바르칸 카드"]
    pick += ["어린 아만 카드", "라자람 카드", "라카이서스 카드", "베히모스 카드", "세헤라데 카드", "칼테이야 카드", "파이어혼 카드"]
    pick += ["클라우디아 카드", "마레가 카드", "마리우 카드", "아이작 카드", "칼리나리 네리아 카드", "베라드 카드", "닐라이 카드"]
    return pick

def server_pick(a="카단"):  # 각 서버명에 맞는 서버번호 리턴하는 함수
    # 우선은 카단서버만 가능
 #   if a == "카단":
 #       return "server=5"
 #   else:
 #       return ""
    return "server=5"

def call_api(server, cards):
    # json으로 불러옴
    headers = {"X-Requested-With": "XMLHttpRequest"}
    url = "https://api.korlark.com/merchants?limit=&" + server
    response = requests.get(url, headers=headers, verify=True)
    data = response.json()
    cardList = ""

    # 현재 시간을 구함
    now = datetime.now()

    for c in data["merchants"]:
        for p in cards:
            if c["card"] == p :
                created_time_str = c["created_at"][:19]  # UTC 시간 문자열에서 초 미만 부분을 제거
                created_time = datetime.strptime(created_time_str, "%Y-%m-%dT%H:%M:%S")  # 문자열에서 datetime 객체로 파싱
                delta = now - created_time
                if delta <= timedelta(minutes=25):  # 25분 이내인지 확인
                    cardList += p + " " + c["continent"] + " " + c["zone"] + " " + c["created_at"] + "\n"

    return cardList

def is_within_range(dt):
    # 현재 시간을 구함
    now = datetime.now()

    # 25분 이내인지 확인
    delta = now - dt
    if delta > timedelta(minutes=25):
        return False
    return True

def main():  # 선택한 카드가 떴으면 카드결과 없으면 '없습니다'출력
    pickcard = card_pick()  # 원하는 카드목록
    pickserver = server_pick()  # 조회원하는 서버
    result = call_api(pickserver, pickcard)

    if result == "":
         return
    else:
         asyncio.run(sendTelegram(result.split('\n')))  # 수정한 sendTelegram 함수를 호출하며, 문자열을 한 줄씩 나누어 리스트로 전달합니다.
 
main()
