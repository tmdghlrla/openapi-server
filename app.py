# import serverless_wsgi

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config

from resources.naver import ChineseResource, NewsSearchResource

# 로그아웃 관련된 임포트문
# from resources.user import jwt_blocklist

app = Flask(__name__)

# 환경변수 셋팅
app.config.from_object(Config)
# JWT 매니저 초기화
jwt=JWTManager(app)

# # 로그아웃된 토큰으로 요청하는 경우 실행되지 않도록 처리하는 코드
# @jwt.token_in_blocklist_loader
# def check_if_token_is_revoked(jwt_header, jwt_payload) :
#     jti = jwt_payload['jti']
#     return jti in jwt_blocklist

api = Api(app)

# 경로와 리소스를 연결한다.
# api.add_resource(,'/user/register') # 회원가입
api.add_resource(ChineseResource, '/chinese')  # 중국어 번역
api.add_resource(NewsSearchResource, '/news')   # 뉴스 검색
# def handler(event, context) :
#     return serverless_wsgi.handle_request(app, event, context)

if __name__ == '__main__' :
    app.run()