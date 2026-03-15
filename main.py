import os
import smtplib
from email.mime.text import MIMEText
from playwright.sync_api import sync_playwright

# --- 設定 ---
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")
TARGET_URL = "https://players.pokemon-card.com/event/detail/953353/1/10349/20260429/1741331"

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg)
        print(f"✅ メール送信成功: {subject}")
    except Exception as e:
        print(f"❌ メール送信失敗: {e}")

def check():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print(f"URL確認中...")
        try:
            page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)
            content = page.content()
            
            # --- 判定とメール送信 ---
            if "先着応募受付中" in content:
                print("✨ 先着応募受付中を見つけました！")
                send_email("【ポケカ：チャンス！】先着応募受付中", 
                           f"予約が可能になっています！今すぐアクセスしてください！\n{TARGET_URL}")
            elif "満席" in content:
                print("● 満席であることを確認しました。")
                send_email("【ポケカ：監視中】現在は満席です", 
                           f"チェックは正常に行われましたが、現在は満席です。\n{TARGET_URL}")
            else:
                print("どちらの文字も見つかりませんでした。")
                send_email("【ポケカ：通知】ステータス不明", 
                           f"サイトの表示が変わった可能性があります。手動で確認してください。\n{TARGET_URL}")
                
        except Exception as e:
            print(f"エラー: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    check()
