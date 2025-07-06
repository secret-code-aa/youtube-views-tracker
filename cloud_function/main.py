import os
import json
import datetime
from google_sheets_tracker import YouTubeTracker
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def youtube_tracker_cloud_function(request):
    """Google Cloud Function 入口點"""
    
    # 設定環境變數
    os.environ['SPREADSHEET_ID'] = os.environ.get('SPREADSHEET_ID', '')
    
    # 建立追蹤器
    tracker = YouTubeTracker()
    
    if not tracker.service:
        return {
            'status': 'error',
            'message': 'Google Sheets API 設定失敗'
        }
    
    # 從環境變數讀取影片列表
    videos_json = os.environ.get('VIDEOS_LIST', '[]')
    videos = json.loads(videos_json)
    
    if not videos:
        return {
            'status': 'error',
            'message': '沒有找到影片列表'
        }
    
    # 執行更新
    try:
        tracker.videos = videos
        tracker.fetch_and_update()
        
        return {
            'status': 'success',
            'message': f'成功更新 {len(videos)} 個影片',
            'timestamp': datetime.datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'更新失敗: {str(e)}'
        } 