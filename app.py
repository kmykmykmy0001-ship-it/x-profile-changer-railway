from flask import Flask, redirect, request, session, url_for
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')  # 세션용, 실제로는 랜덤으로 변경

# X API 설정 (v1.1 for update_profile, Tweepy 사용)
@app.route('/')
def home():
    return '''
    <h1>X 프로필 변경기</h1>
    <p>아래 버튼 클릭하면 X 로그인 후 이름과 프사가 자동으로 바뀝니다!</p>
    <a href="/login"><button style="padding:10px; font-size:16px;">X 로그인 & 업데이트</button></a>
    <p><small>변경 내용: 이름 = "ㅋㅋㅋ", 프사 = 웃는 고양이 밈</small></p>
    '''

@app.route('/login')
def login():
    try:
        auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_SECRET'), secure=True)
        redirect_url = auth.get_authorization_url(signin_with_twitter=True)
        session['oauth_token'] = auth.oauth_token
        session['oauth_token_secret'] = auth.oauth_token_secret
        return redirect(redirect_url)
    except tweepy.TweepyException as e:
        return f"로그인 오류: {e}"

@app.route('/callback')
def callback():
    try:
        auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_SECRET'))
        auth.set_access_token(session['oauth_token'], session['oauth_token_secret'])
        verifier = request.args.get('oauth_verifier')
        auth.get_access_token(verifier)
        
        # API 클라이언트 생성 (업데이트용)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        
        # 프로필 업데이트 (이름과 프사 URL)
        api.update_profile(name="ㅋㅋㅋ")  # 새 이름
        # 프사: 미리 업로드된 이미지 URL 사용 (Railway에 이미지 파일 추가하거나 외부 URL)
        api.update_profile_image("https://i.imgur.com/funny-cat-meme.jpg")  # 예시 URL – 실제로 바꾸세요 (Imgur 등에 웃는 고양이 업로드)
        
        return '''
        <h1>성공!</h1>
        <p>프로필이 업데이트되었습니다. X 앱/웹 새로고침 후 확인하세요. (지연 1-2분)</p>
        <a href="https://x.com">X로 이동</a>
        '''
    except tweepy.TweepyException as e:
        return f"업데이트 오류: {e}. API 키 확인하세요."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
