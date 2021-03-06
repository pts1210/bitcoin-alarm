import requests
import pandas as pd
import time
import webbrowser
import numpy as np

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)

myToken = "xoxb-mytoken"
post_message(myToken,"#bitcoin-alarm","start")

a = 1


while True:
    
    def rsiindex(symbol):
        url = "https://api.upbit.com/v1/candles/minutes/10" #### minutes 뒤에 원하는 분 설정을 넣으면 된다 기본적으로 3분으로 설정
    
        querystring = {"market":symbol,"count":"500"}
    
        response = requests.request("GET", url, params=querystring)
    
        data = response.json()
    
        df = pd.DataFrame(data)
    
        df=df.reindex(index=df.index[::-1]).reset_index()
    
        df['close']=df["trade_price"]
        
        global a
    
        if a==1:
 
         
            a=2   

    
    
        def rsi(ohlc: pd.DataFrame, period: int = 14):
            ohlc["close"] = ohlc["close"]
            delta = ohlc["close"].diff()
    
            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0
    
            _gain = up.ewm(com=(period - 1), min_periods=period).mean()
            _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
    
            RS = _gain / _loss
            return pd.Series(100 - (100 / (1 + RS)), name="RSI")
    
        rsi = rsi(df, 14).iloc[-1]
        print(symbol)
        print('upbit 10 minute RSI:', rsi)
        print('')
        if rsi<30:     ######## rsi 지수가 30미만이면 Slack을 통해 메시지 전송 ,원하는 숫자로 수정가능
            post_message(myToken,"#bitcoin-alarm","KRW-BTC :" + str(round(rsi,3))) 
        elif rsi>65:
            post_message(myToken,"#bitcoin-alarm","KRW-BTC :" + str(round(rsi,3)))
        time.sleep(60)
      

    def stockrsi(symbol):
        url = "https://api.upbit.com/v1/candles/minutes/10"
        
        querystring = {"market":symbol,"count":"500"}
        
        response = requests.request("GET", url, params=querystring)
        
        data = response.json()
        
        df = pd.DataFrame(data)
        
        series=df['trade_price'].iloc[::-1]
        
        df = pd.Series(df['trade_price'].values)
    
        period=14
        smoothK=3
        smoothD=3
         
        delta = series.diff().dropna()
        ups = delta * 0
        downs = ups.copy()
        ups[delta > 0] = delta[delta > 0]
        downs[delta < 0] = -delta[delta < 0]
        ups[ups.index[period-1]] = np.mean( ups[:period] )
        ups = ups.drop(ups.index[:(period-1)])
        downs[downs.index[period-1]] = np.mean( downs[:period] )
        downs = downs.drop(downs.index[:(period-1)])
        rs = ups.ewm(com=period-1,min_periods=0,adjust=False,ignore_na=False).mean() / \
             downs.ewm(com=period-1,min_periods=0,adjust=False,ignore_na=False).mean() 
        rsi = 100 - 100 / (1 + rs)
    
        stochrsi  = (rsi - rsi.rolling(period).min()) / (rsi.rolling(period).max() - rsi.rolling(period).min())
        stochrsi_K = stochrsi.rolling(smoothK).mean()
        stochrsi_D = stochrsi_K.rolling(smoothD).mean()
        
        print(symbol)    
       
        print('')
        time.sleep(1)

 
    rsiindex("KRW-BTC")   ###원하는 코인종목을 밑에 추가해주면 추가가된다 #기본적으로 비트,도지,이클,이더,리플
    stockrsi("KRW-BTC")
