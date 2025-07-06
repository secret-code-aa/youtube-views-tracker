import requests
import re
import json
from typing import Optional

def fetch_youtube_views(video_url: str) -> Optional[int]:
    """
    Fetch the view count of a YouTube video given its URL.
    Returns the view count as an integer, or None if not found.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(video_url, headers=headers)
        if response.status_code != 200:
            return None
        
        # 嘗試多種方式來找到觀看數
        content = response.text
        
        # 方法1: 尋找 ytInitialData 中的觀看數
        yt_data_match = re.search(r'var ytInitialData = ({.*?});', content)
        if yt_data_match:
            try:
                yt_data = json.loads(yt_data_match.group(1))
                # 在 ytInitialData 中尋找觀看數
                views = extract_views_from_yt_data(yt_data)
                if views:
                    return views
            except json.JSONDecodeError:
                pass
        
        # 方法2: 直接搜尋觀看數模式
        patterns = [
            r'"viewCount":"(\d+)"',
            r'"viewCount":\{"simpleText":"([\d,]+) views"\}',
            r'"viewCount":\{"runs":\[\{"text":"([\d,]+) views"\}\]\}',
            r'([\d,]+) views',
            r'([\d,]+)次觀看'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                view_str = match.group(1).replace(',', '')
                try:
                    return int(view_str)
                except ValueError:
                    continue
                    
    except Exception as e:
        print(f"Error fetching YouTube views: {e}")
    return None

def extract_views_from_yt_data(yt_data):
    """從 ytInitialData 中提取觀看數"""
    try:
        # 嘗試多個可能的路徑
        paths = [
            ['contents', 'twoColumnWatchNextResults', 'results', 'results', 'contents', 0, 'videoPrimaryInfoRenderer', 'viewCount', 'videoViewCountRenderer', 'viewCount', 'simpleText'],
            ['contents', 'twoColumnWatchNextResults', 'results', 'results', 'contents', 0, 'videoPrimaryInfoRenderer', 'viewCount', 'videoViewCountRenderer', 'viewCount', 'runs', 0, 'text'],
            ['contents', 'twoColumnWatchNextResults', 'results', 'results', 'contents', 0, 'videoPrimaryInfoRenderer', 'viewCount', 'videoViewCountRenderer', 'viewCount', 'simpleText']
        ]
        
        for path in paths:
            try:
                value = yt_data
                for key in path:
                    value = value[key]
                # 提取數字
                view_str = re.search(r'([\d,]+)', value)
                if view_str:
                    return int(view_str.group(1).replace(',', ''))
            except (KeyError, TypeError, IndexError):
                continue
    except Exception:
        pass
    return None 