from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt
from flask_restful import Resource
import requests
from config import Config
from mysql_connection import get_connection
from mysql.connector import Error


class ChineseResource(Resource) :
    def post(self) :
        data = request.get_json()

        # 네이버의 파파고 API를 호출하여 결과를 가져온다.
        # 파파고 API의 문서를 보고 어떤 데이터를 보내야하는지 파악하여
        # reuqests의 get, post, put, delete 등의 함수를 이용하여 호출하면 된다.
        req_data = {
                    "source": "ko",
                    "target": "zh-CN",
                    "text": data['sentence']
                    }
        
        req_header = {"X-Naver-Client-Id" : Config.X_NAVER_CLIENT_ID,
                      "X-Naver-Client-Secret" : Config.X_NAVER_CLIENT_SECRET}
        
        response = requests.post("https://openapi.naver.com/v1/papago/n2mt",
                      req_data, 
                      headers= req_header)
        
        # 데이터를 파파고 서버로 부터 받아왔으니 우리가 필요하나 데이터만 뽑아내면 된다.
        
        print(response)

        # 받아온 데이터를 json형태로 변환
        response = response.json()
        print(response)

        chinese = response['message']['result']['translatedText']

        return {"result" : "success",
                "chinese" : chinese}, 200
    
class NewsSearchResource(Resource) :
    def get(self) :
        keyword = request.args.get('keyword')

        req_string = {'query' : keyword,
                      'display' : 30,
                      'sord' : 'date'
        }

        req_header =  {"X-Naver-Client-Id" : Config.X_NAVER_CLIENT_ID,
                      "X-Naver-Client-Secret" : Config.X_NAVER_CLIENT_SECRET
        }

        response = requests.get("https://openapi.naver.com/v1/search/news.json?query=코로나",
                                req_string,
                                headers= req_header
                                )
        print(response)
        response = response.json()
        print(response)

        return {"result": "success",
                "items" : response['items'],
                'count' : len(response['items'])}, 200