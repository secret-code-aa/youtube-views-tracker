from fetch_youtube_views import fetch_youtube_views

def main():
    print("YouTube 觀看數抓取示範")
    print("=" * 30)
    
    # 讓使用者輸入自己的影片 URL
    print("請輸入你的 YouTube 影片 URL:")
    print("範例: https://www.youtube.com/watch?v=你的影片ID")
    
    while True:
        video_url = input("\n請貼上 YouTube 影片 URL (或輸入 'quit' 結束): ").strip()
        
        if video_url.lower() == 'quit':
            break
            
        if not video_url.startswith('https://www.youtube.com/watch?v='):
            print("❌ 請輸入有效的 YouTube 影片 URL")
            continue
            
        print(f"\n正在抓取觀看數...")
        views = fetch_youtube_views(video_url)
        
        if views:
            print(f"✅ 觀看數: {views:,}")
        else:
            print("❌ 無法取得觀看數")
        
        print("-" * 30)

if __name__ == "__main__":
    main() 