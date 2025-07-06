import os
import datetime
from google_sheets_tracker import YouTubeTracker
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def main():
    print("YouTube 觀看數手動更新工具")
    print("=" * 40)
    
    # 檢查必要設定
    if not os.getenv('SPREADSHEET_ID'):
        print("❌ 請在 .env 檔案中設定 SPREADSHEET_ID")
        return
    
    if not os.path.exists('credentials.json'):
        print("❌ 請先下載 credentials.json 檔案")
        return
    
    # 建立追蹤器
    tracker = YouTubeTracker()
    
    if not tracker.service:
        print("❌ Google Sheets API 設定失敗")
        return
    
    # 從檔案讀取影片列表
    videos = load_videos_from_file()
    
    if not videos:
        print("❌ 沒有找到影片列表，請先設定 videos.txt")
        return
    
    # 執行更新
    print(f"\n🕐 開始更新 - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 要更新的影片數量: {len(videos)}")
    
    tracker.videos = videos
    tracker.fetch_and_update()
    
    print("\n✅ 更新完成！")
    print("💡 下次要更新時，再次執行這個程式即可")

def load_videos_from_file():
    """從檔案讀取影片列表"""
    videos = []
    
    if not os.path.exists('videos.txt'):
        print("📝 建立 videos.txt 檔案...")
        create_videos_file()
        return []
    
    try:
        with open('videos.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('|')
                    if len(parts) >= 1:
                        video_url = parts[0].strip()
                        video_title = parts[1].strip() if len(parts) > 1 else ""
                        
                        if video_url.startswith('https://www.youtube.com/watch?v='):
                            video_id = video_url.split('v=')[1].split('&')[0]
                            videos.append({
                                'url': video_url,
                                'id': video_id,
                                'title': video_title
                            })
    except Exception as e:
        print(f"❌ 讀取 videos.txt 時發生錯誤: {e}")
    
    return videos

def create_videos_file():
    """建立影片列表檔案"""
    content = """# YouTube 影片列表
# 格式：影片URL|影片標題（可選）
# 範例：
# https://www.youtube.com/watch?v=dQw4w9WgXcQ|我的影片標題
# https://www.youtube.com/watch?v=9bZkp7q19f0|另一個影片

# 請在下面加入你的影片 URL：
"""
    
    with open('videos.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 已建立 videos.txt 檔案")
    print("📝 請編輯 videos.txt 檔案，加入你要追蹤的影片 URL")

if __name__ == "__main__":
    main() 