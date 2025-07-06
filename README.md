# YouTube 觀看數自動追蹤系統

這個系統可以自動抓取 YouTube 影片觀看數，並每週更新到 Google Sheets。

## 🚀 功能特色

- ✅ 自動抓取 YouTube 影片觀看數
- ✅ 自動更新到 Google Sheets
- ✅ 每週自動排程執行
- ✅ 支援多個影片同時追蹤
- ✅ 歷史資料追蹤

## 📋 安裝步驟

### 1. 安裝 Python 套件

```bash
pip install -r requirements.txt
```

### 2. 設定 Google Sheets API

#### 步驟 1: 建立 Google Cloud 專案
1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 啟用 Google Sheets API

#### 步驟 2: 建立憑證
1. 在 Google Cloud Console 中，前往「API 和服務」>「憑證」
2. 點選「建立憑證」>「OAuth 2.0 用戶端 ID」
3. 選擇「桌面應用程式」
4. 下載 JSON 憑證檔案
5. 將檔案重新命名為 `credentials.json` 並放在專案根目錄

#### 步驟 3: 建立 Google Sheets
1. 前往 [Google Sheets](https://sheets.google.com/)
2. 建立新的空白試算表
3. 複製試算表 ID（網址中的長字串）
4. 建立 `.env` 檔案並加入：
   ```
   SPREADSHEET_ID=你的試算表ID
   ```

### 3. 設定檔案結構

```
project/
├── credentials.json     # Google API 憑證
├── .env                # 環境變數
├── requirements.txt    # Python 套件
├── fetch_youtube_views.py
├── google_sheets_tracker.py
└── README.md
```

## 🎯 使用方式

### 快速測試
```bash
python demo.py
```

### 自動追蹤系統
```bash
python google_sheets_tracker.py
```

## 📊 Google Sheets 格式

系統會自動建立以下格式的試算表：

| 日期 | 影片ID | 影片標題 | 觀看數 |
|------|--------|----------|--------|
| 2024-01-15 | dQw4w9WgXcQ | 我的影片 | 1,234,567 |
| 2024-01-22 | dQw4w9WgXcQ | 我的影片 | 1,345,678 |

## ⚙️ 進階設定

### 修改更新頻率
在 `google_sheets_tracker.py` 中修改：
```python
# 每週一上午 9:00
schedule.every().monday.at("09:00").do(self.fetch_and_update)

# 改為每天上午 9:00
schedule.every().day.at("09:00").do(self.fetch_and_update)

# 改為每小時執行
schedule.every().hour.do(self.fetch_and_update)
```

### 自訂欄位
可以修改 `create_header()` 和 `fetch_and_update()` 方法來新增更多欄位，例如：
- 訂閱數
- 按讚數
- 留言數
- 分享數

## 🔧 故障排除

### 常見問題

1. **憑證錯誤**
   - 確認 `credentials.json` 檔案存在且格式正確
   - 重新下載憑證檔案

2. **權限錯誤**
   - 確認 Google Sheets 已分享給你的 Google 帳號
   - 確認試算表 ID 正確

3. **觀看數抓取失敗**
   - 確認影片 URL 正確
   - 確認影片是公開的
   - 檢查網路連線

### 重新授權
如果遇到授權問題，刪除 `token.json` 檔案並重新執行程式。

## 📈 資料分析建議

### 使用 Google Sheets 內建功能
1. **建立圖表**：選取資料 > 插入 > 圖表
2. **計算成長率**：使用公式計算週間成長
3. **設定條件格式**：標示重要數據

### 進階分析
可以將資料匯出到其他工具進行更深入的分析：
- Google Data Studio
- Excel
- Python pandas

## 🤝 貢獻

歡迎提出建議和改進意見！

## 📄 授權

MIT License 