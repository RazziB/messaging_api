from handlers.login_handler import LoginHandler
from handlers.messages_handler import MessagesHandler
from handlers.register_handler import RegisterHandler
from handlers.sid_handler import SIDHandler


class ApiHandler:
    def __init__(self):
        self.messages_handler = MessagesHandler()
        self.register_handler = RegisterHandler()
        self.login_handler = LoginHandler()
        self.sid_handler = SIDHandler()

#
# headers = {
#     'Host': 'sdarot.tw',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0',
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
#     'Accept-Language': 'en-US,en;q=0.5',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Referer': 'https://sdarot.tw/',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'X-Requested-With': 'XMLHttpRequest',
#     'Content-Length': '75',
#     'Origin': 'https://sdarot.tw',
#     'Connection': 'keep-alive',
#     'Cookie': 'Sdarot=qpoVQFUfAZHAi6dTffu4RQ4lpVHy0Q4nbDSly7kJXX0xII-KRL8LTBdvn8vPM66LVvI7KVRwNVW9CbaJG2-EHm%2CAWFYo0wQcHsqU-EZciV%2C2VAw%2CFp8dhmiyRhyNTii3; _ga=GA1.2.354103578.1665689464; _gid=GA1.2.993802485.1665689464; _gat=1',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-origin',
#     'TE': 'trailers'
# }
# url = 'https://sdarot.tw/ajax/watch'
#
# payload = 'watch=false&token=63486cfb36303&serie=1508&season=4&episode=10&type=episode'
#
# import requests
# response = requests.post(url=url, data=payload, headers=headers)
# a = response.status_code
