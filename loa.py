import requests
from datetime import datetime
import telegram as tel
import asyncio


async def sendTelegram(result):
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


def card_pick():  # 호출 원하는 카드 목록 불러오는 함수
    # 우선은 하드코딩으로 목록화해두자
    pick = []
    pick.append("어린 아만 카드")
    pick.append("에버그레이스 카드")
    pick.append("웨이 카드")
    pick.append("클라우디아 카드" )
    pick.append("라자람 카드")
    pick.append("라카이서스 카드")
    pick.append("바르칸 카드")
    pick.append("베히모스 카드") 
    pick.append("세헤라데 카드")
    pick.append("칼테이야 카드")
    pick.append("파이어혼 카드")
    pick.append("마레가 카드")
    pick.append("마리우 카드")
    pick.append("아이작 카드")
    pick.append("칼리나리 네리아 카드") 
    pick.append("베라드 카드")
    pick.append("닐라이 카드")
    
    return pick
    # global pickitem = ['전설 호감도']


def server_pick(a="카단"):  # 각 서버명에 맞는 서버번호 리턴하는 함수
    # 우선은 카단서버만 가능
 #   if a == "카단":
 #       return "server=5"
 #   else:
 #       return ""
    return "server=5"

def call_api(server, cards, cardcount):  # Kloa.gg 에서 api이용하여 카드 떴는지 확인하여 뜬 카드 있으면 리턴
    # json으로 불러옴
    headers = {"X-Requested-With": "XMLHttpRequest"}
    url = "https://api.korlark.com/merchants?limit=" + cardcount + "&" + server
    response = requests.get(url, headers=headers, verify=False)
    data = response.json()
    cardList = ""

    for c in data["merchants"]:
        d=len(data["merchants"]) 
        for p in cards:
            if c["card"] == p :
                cardList = cardList+ p + " " + c["continent"] + " " + c["zone"] + " " + c["created_at"]
                d = d -1
                if  d  > 0:
                    cardList = cardList + "\n"

    return cardList


def main():  # 선택한 카드가 떴으면 카드결과 없으면 '없습니다'출력
    merchantCount = {
        0: 12, 12: 12,
        1: 6,  13: 5,
        2: 8,  14: 8,
        3: 6,  15: 7,
        4: 10,   16: 10,
        5: 13,   17: 13,
        6: 3,  18: 13,
        7: 10,  19: 10,
        8: 12,   20: 12,
        9: 9,  21: 9,
        10: 5, 22: 5,
        11: 6,  23: 6,
    }  # 시간별 떠상숫자 하드코딩
    cardcount = str(merchantCount[datetime.now().hour])
    pickcard = card_pick()  # 원하는 카드목록
    pickserver = server_pick()  # 조회원하는 서버
    result = call_api(pickserver, pickcard, cardcount)

    if result == "":
         return
    else:
         asyncio.run(sendTelegram(result.split('\n')))  # 수정한 sendTelegram 함수를 호출하며, 문자열을 한 줄씩 나누어 리스트로 전달합니다.
 

if __name__ == "__main__":  # 직접실행시 main()호출
    # SSL워닝 끄기
    requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning
    )

    main()
