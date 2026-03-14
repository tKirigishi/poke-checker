import os
import smtplib
from email.mime.text import MIMEText
from playwright.sync_api import sync_playwright

# --- 設定（GitHubのSecretsから自動で読み込まれます） ---
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")
TARGET_URL = "https://players.pokemon-card.com/event/detail/953353/1/10349/20260429/1741331"

def send_email(subject, body):
    """Gmailを使用して通知メールを送信する関数"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL
    
    try:
        # SSL（ポート465）でGmailサーバーに接続
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg)
        print("✅ 通知メールを送信しました。")
    except Exception as e:
        print(f"❌ メール送信エラー: {e}")

def check():
    """サイトを巡回してステータスを確認する関数"""
    with sync_playwright() as p:
        # ブラウザを起動（GitHub Actions上で動くように設定）
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print(f"[{TARGET_URL}] にアクセス中...")
        try:
            # ページ読み込み（ネットワークが落ち着くまで待機）
            page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)
            
            # ページ全体のテキストを取得
            content = page.content()
            
            # 「先着応募受付中」が含まれているか判定
            # ※「満席」から「先着応募受付中」に変わった瞬間を検知します
            if "先着応募受付中" in content:
                print("✨✨✨ 空席（応募受付中）を発見しました！ ✨✨✨")
                subject = "【ポケカ予約】空きが出た可能性があります！"
                body = f"ポケカ公式サイトで「先着応募受付中」を確認しました。\n至急確認してください！\n\nURL: {TARGET_URL}"
                send_email(subject, body)
            else:
                print("確認完了：現在は満席、または受付期間外です。")
                
        except Exception as e:
            print(f"❌ サイトアクセス中にエラーが発生しました: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    check()
