import requests
import re
import json
from typing import List, Dict, Optional
from fetch_youtube_views import fetch_youtube_views

def get_channel_videos(channel_url: str) -> List[Dict]:
    """
    從頻道頁面獲取影片列表
    注意：這需要頻道頁面的 HTML 結構，可能需要根據實際情況調整
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(channel_url, headers=headers)
        
        if response.status_code != 200:
            return []
        
        content = response.text
        
        # 尋找影片 ID 的模式
        video_pattern = r'watch\?v=([a-zA-Z0-9_-]{11})'
        video_ids = re.findall(video_pattern, content)
        
        # 去重並轉換為完整 URL
        unique_video_ids = list(set(video_ids))
        videos = []
        
        for video_id in unique_video_ids[:10]:  # 限制前10個影片避免過度請求
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append({
                'id': video_id,
                'url': video_url
            })
        
        return videos
        
    except Exception as e:
        print(f"Error getting channel videos: {e}")
        return []

def analyze_channel(channel_url: str):
    """
    分析整個頻道的影片觀看數
    """
    print(f"正在分析頻道: {channel_url}")
    print("=" * 50)
    
    # 獲取頻道影片列表
    videos = get_channel_videos(channel_url)
    
    if not videos:
        print("❌ 無法獲取頻道影片列表")
        print("💡 提示：請確保頻道是公開的，或者直接提供影片 URL 列表")
        return
    
    print(f"找到 {len(videos)} 個影片")
    print("-" * 50)
    
    total_views = 0
    video_data = []
    
    for i, video in enumerate(videos, 1):
        print(f"正在處理影片 {i}/{len(videos)}: {video['id']}")
        
        views = fetch_youtube_views(video['url'])
        
        if views:
            total_views += views
            video_data.append({
                'id': video['id'],
                'url': video['url'],
                'views': views
            })
            print(f"✅ 觀看數: {views:,}")
        else:
            print("❌ 無法取得觀看數")
        
        print("-" * 30)
    
    # 顯示統計結果
    print("\n📊 頻道統計結果")
    print("=" * 50)
    print(f"總影片數: {len(videos)}")
    print(f"成功抓取: {len(video_data)}")
    print(f"總觀看數: {total_views:,}")
    if video_data:
        avg_views = total_views // len(video_data)
        print(f"平均觀看數: {avg_views:,}")
    
    return video_data

def main():
    print("YouTube 頻道分析器")
    print("=" * 30)
    
    print("請選擇模式:")
    print("1. 分析整個頻道")
    print("2. 手動輸入影片 URL 列表")
    
    choice = input("\n請選擇 (1 或 2): ").strip()
    
    if choice == "1":
        channel_url = input("\n請輸入你的 YouTube 頻道 URL: ").strip()
        if channel_url:
            analyze_channel(channel_url)
        else:
            print("❌ 請輸入有效的頻道 URL")
    
    elif choice == "2":
        print("\n請輸入你的影片 URL 列表 (每行一個，輸入 'done' 結束):")
        video_urls = []
        
        while True:
            url = input().strip()
            if url.lower() == 'done':
                break
            if url.startswith('https://www.youtube.com/watch?v='):
                video_urls.append(url)
            else:
                print("❌ 請輸入有效的 YouTube 影片 URL")
        
        if video_urls:
            print(f"\n正在分析 {len(video_urls)} 個影片...")
            total_views = 0
            
            for i, url in enumerate(video_urls, 1):
                print(f"\n影片 {i}/{len(video_urls)}")
                views = fetch_youtube_views(url)
                if views:
                    total_views += views
                    print(f"✅ 觀看數: {views:,}")
                else:
                    print("❌ 無法取得觀看數")
            
            print(f"\n📊 總觀看數: {total_views:,}")
        else:
            print("❌ 沒有輸入有效的影片 URL")
    
    else:
        print("❌ 無效的選擇")

if __name__ == "__main__":
    main() 