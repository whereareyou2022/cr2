import requests
import json
import xmltodict
import html
import os
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

# github라는 오픈소스 공간에서 SLACK_WEBHOOK_URL을 암호화하기 위한 코드..
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')

todaynow = datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d %H:%M")

def makeSection(data):
  return    {
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": f"{data}"
            }
          }
        ]
      }

def callWebhook (payload):
  URL = SLACK_WEBHOOK_URL
  headers = {
    'Content-type' : 'application/json',
  }
  res = requests.post(URL, headers=headers, json=payload)

  print("data : " + res.text)

def getTotalData():
  url = "https://coinmarketcap.com/ko/gainers-losers/"
  response = requests.get(url)

  if response.status_code == 200:
      html = response.text
      soup = BeautifulSoup(html, 'html.parser')
      content1 = soup.select_one('#__next > div > div.main-content > div.bywovg-0.kuGegY > div:nth-of-type(1) > div > div.sc-5tazol-0.bepHND > div > div:nth-of-type(1) > span:nth-of-type(4) > a')
      content2 = soup.select_one('#__next > div > div.main-content > div.bywovg-0.kuGegY > div:nth-of-type(2) > div > div > div > div.cmc-global-stats__content > div > span:nth-of-type(5) > a')

      volume = "24시간 거래량 : " + content1.text
      dominance = "도미넌스 : " + content2.text

      return "*:ballot_box_with_check: 시장 상황*\n\n"+ volume + "\n" + dominance
  else:
      return None

def getUpCoinData():
  url = "https://coinmarketcap.com/ko/gainers-losers/"
  response = requests.get(url)

  if response.status_code == 200:
      html = response.text
      soup = BeautifulSoup(html, 'html.parser')
      contents = soup.select('#__next > div > div.main-content > div.sc-57oli2-0.comDeo.cmc-body-wrapper > div > div.sc-1yw69nc-0.DaVcG.table-wrap > div > div:nth-of-type(1) > div > table > tbody > tr')
      result = ""

      for idx in range(0, 10):

          info = ":medal:*"+str(idx + 1)+"위 급등 코인* → " + contents[idx].select_one('td:nth-of-type(2) > a > div > div > p').text
          name = "코드 : " + contents[idx].select_one('td:nth-of-type(2) > a > div > div > div > p').text
          rate = "상승 : " + contents[idx].select_one('td:nth-of-type(4) > span').text
          price = "시세 : " + contents[idx].select_one('td:nth-of-type(3) > span').text
          result += info +"\n" + name + "\n" + rate + "\n" + price + "\n\n"

      return "*:white_check_mark: 급등코인 종목 top3*\n\n"+ result

  else:
      return None

def getDownCoinData():
  url = "https://coinmarketcap.com/ko/gainers-losers/"
  response = requests.get(url)

  if response.status_code == 200:
      html = response.text
      soup = BeautifulSoup(html, 'html.parser')
      contents = soup.select('#__next > div > div.main-content > div.sc-57oli2-0.comDeo.cmc-body-wrapper > div > div.sc-1yw69nc-0.DaVcG.table-wrap > div > div:nth-of-type(2) > div > table > tbody > tr')
      result = ""

      for idx in range(0, 3):

          info = ":medal:*"+str(idx + 1)+"위 급락 코인* → " + contents[idx].select_one('td:nth-of-type(2) > a > div > div > p').text
          name = "코드 : " + contents[idx].select_one('td:nth-of-type(2) > a > div > div > div > p').text
          rate = "하락 : -" + contents[idx].select_one('td:nth-of-type(4) > span').text
          price = "시세 : " + contents[idx].select_one('td:nth-of-type(3) > span').text
          result += info +"\n" + name + "\n" + rate + "\n" + price + "\n\n"

      return "*:white_check_mark: 급락코인 종목 top3*\n\n"+ result
  else:
      return None


def main():
  print(f'\n\n[system] 24시간 거래량, 도미넌스(BTC/ETH) 데이터를 불러오고 있습니다.')
  totalData = getTotalData()
  totalPayload = makeSection(totalData)


  print(f'\n\n[system] 급등코인 10개 종목을 불러오고 있습니다.')
  upCoinData = getUpCoinData()
  upCoinPayload = makeSection(upCoinData)

  print(f'\n\n[system] 급락코인 10개 종목을 불러오고 있습니다.')
  downCoinData = getDownCoinData()
  downCoinPayload = makeSection(downCoinData)

  print(f'\n\n[system] SLACK 발송을 시작합니다...\n\n')

  callWebhook(
    {  
        "blocks": [
        {
          "type": "divider"
        },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*:coin: 암호화폐 시장분석 ({todaynow})*\n\n "
                }
            }, 
        {
          "type": "divider"
        }
      ]
    }
  )
  callWebhook(totalPayload)
  callWebhook(
    {  
        "blocks": [
        {
          "type": "divider"
        }
      ]
    }
  )
  callWebhook(upCoinPayload)
  callWebhook(
    {  
        "blocks": [
        {
          "type": "divider"
        }
      ]
    }
  )
  callWebhook(downCoinPayload)

if __name__ == "__main__":
  main()
