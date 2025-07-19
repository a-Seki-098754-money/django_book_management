# book_management/mail.py
import os
from smtplib import SMTP
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header # Headerクラスをインポート

def send_mail(to, subject, body):
    ID = 'あなたのGmailアドレス' # ここにあなたのGmailアドレスを設定してください
    PASS = os.environ.get('MAIL_PASS') 
    
    if not PASS:
        print("Error: MAIL_PASS environment variable is not set.")
        return False

    HOST = 'smtp.gmail.com'
    PORT = 587
    
    msg = MIMEMultipart()
    
    # HTML形式のボディをUTF-8でエンコード
    msg.attach(MIMEText(body, 'html', 'utf-8')) 
    
    # 件名をUTF-8でエンコード
    msg['Subject'] = Header(subject, 'utf-8')
    
    # --- ここを修正 ---
    # Fromヘッダーの名前部分をUTF-8でエンコード
    from_name = "図書管理システム"
    # formataddrの第一引数にHeaderオブジェクトをstr()で渡す
    msg['From'] = formataddr((str(Header(from_name, 'utf-8')), ID)) 
    # --- 修正ここまで ---
    
    # 'to' がリストの場合、カンマ区切りの文字列に変換
    if isinstance(to, list):
        msg['To'] = ", ".join(to)
    else:
        msg['To'] = to
    
    try:
        # 送信処理
        server = SMTP(HOST, PORT)
        server.starttls() 
        server.login(ID, PASS) 
        
        server.send_message(msg) 
        server.quit() 
        return True
    except Exception as e:
        print(f"メール送信エラー: {e}")
        return False
