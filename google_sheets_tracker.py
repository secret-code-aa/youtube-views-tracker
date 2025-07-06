import os
import json
import datetime
import schedule
import time
from typing import List, Dict
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fetch_youtube_views import fetch_youtube_views
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# Google Sheets API 設定
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')  # 你的 Google Sheets ID
CREDENTIALS_FILE = 'credentials.json'  # Google API 憑證檔案
TOKEN_FILE = 'token.json'  # 儲存授權 token

class YouTubeTracker:
    def __init__(self):
        self.service = None
        self.videos = []
        self.setup_google_sheets()
    
    def setup_google_sheets(self):
        """設定 Google Sheets API 連線"""
        creds = None
        
        # 載入已存在的 token
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
        # 如果沒有有效的憑證，進行授權
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    print("❌ 請先下載 credentials.json 檔案")
                    print("💡 請參考 README.md 的設定說明")
                    return
                
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # 儲存憑證
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('sheets', 'v4', credentials=creds)
        print("✅ Google Sheets API 連線成功")
    
    def add_video(self, video_url: str, video_title: str = ""):
        """新增要追蹤的影片"""
        video_id = video_url.split('v=')[1].split('&')[0]
        self.videos.append({
            'url': video_url,
            'id': video_id,
            'title': video_title
        })
        print(f"✅ 新增影片: {video_title or video_id}")
    
    def get_current_data(self) -> List[List]:
        """從 Google Sheets 取得現有資料"""
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range='A:D'
            ).execute()
            return result.get('values', [])
        except HttpError as error:
            print(f"❌ 無法讀取 Google Sheets: {error}")
            return []
    
    def update_sheet(self, data: List[List]):
        """更新 Google Sheets"""
        try:
            body = {
                'values': data
            }
            result = self.service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range='A:D',
                valueInputOption='RAW',
                body=body
            ).execute()
            print(f"✅ 已更新 {result.get('updatedCells')} 個儲存格")
        except HttpError as error:
            print(f"❌ 無法更新 Google Sheets: {error}")
    
    def create_header(self):
        """建立表頭"""
        return [
            ['日期', '影片ID', '影片標題', '觀看數']
        ]
    
    def fetch_and_update(self):
        """抓取觀看數並更新到 Google Sheets"""
        print(f"\n🕐 開始更新 - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 取得現有資料
        existing_data = self.get_current_data()
        
        # 如果沒有資料，建立表頭
        if not existing_data:
            existing_data = self.create_header()
        
        # 準備新資料
        new_rows = []
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        for video in self.videos:
            print(f"正在處理: {video['title'] or video['id']}")
            
            views = fetch_youtube_views(video['url'])
            
            if views:
                new_row = [
                    current_date,
                    video['id'],
                    video['title'] or video['id'],
                    views
                ]
                new_rows.append(new_row)
                print(f"✅ 觀看數: {views:,}")
            else:
                print("❌ 無法取得觀看數")
        
        # 合併資料並更新
        if new_rows:
            all_data = existing_data + new_rows
            self.update_sheet(all_data)
            print(f"✅ 成功更新 {len(new_rows)} 筆資料")
        else:
            print("❌ 沒有新資料可更新")
    
    def run_scheduler(self):
        """執行排程器"""
        print("🚀 啟動自動追蹤系統")
        print("📅 每週一上午 9:00 自動更新")
        
        # 設定每週一上午 9:00 執行
        schedule.every().monday.at("09:00").do(self.fetch_and_update)
        
        # 立即執行一次
        self.fetch_and_update()
        
        # 持續執行排程
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分鐘檢查一次

def main():
    print("YouTube 觀看數自動追蹤系統")
    print("=" * 40)
    
    # 檢查必要設定
    if not SPREADSHEET_ID:
        print("❌ 請在 .env 檔案中設定 SPREADSHEET_ID")
        return
    
    if not os.path.exists(CREDENTIALS_FILE):
        print("❌ 請先下載 credentials.json 檔案")
        print("💡 請參考 README.md 的設定說明")
        return
    
    # 建立追蹤器
    tracker = YouTubeTracker()
    
    if not tracker.service:
        print("❌ Google Sheets API 設定失敗")
        return
    
    # 新增要追蹤的影片
    print("\n請新增要追蹤的影片:")
    while True:
        video_url = input("\n請輸入 YouTube 影片 URL (或輸入 'done' 結束): ").strip()
        
        if video_url.lower() == 'done':
            break
        
        if not video_url.startswith('https://www.youtube.com/watch?v='):
            print("❌ 請輸入有效的 YouTube 影片 URL")
            continue
        
        video_title = input("請輸入影片標題 (可選): ").strip()
        tracker.add_video(video_url, video_title)
    
    if not tracker.videos:
        print("❌ 沒有新增任何影片")
        return
    
    # 選擇執行模式
    print("\n請選擇執行模式:")
    print("1. 立即執行一次")
    print("2. 啟動自動排程 (每週一上午 9:00)")
    
    choice = input("\n請選擇 (1 或 2): ").strip()
    
    if choice == "1":
        tracker.fetch_and_update()
    elif choice == "2":
        tracker.run_scheduler()
    else:
        print("❌ 無效的選擇")

if __name__ == "__main__":
    main() 