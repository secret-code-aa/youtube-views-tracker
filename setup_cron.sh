#!/bin/bash

# 設定 cron job 來定期執行 YouTube 追蹤器
# 這個方法需要電腦保持開機狀態

echo "設定 YouTube 觀看數追蹤的 cron job..."

# 取得當前目錄的絕對路徑
CURRENT_DIR=$(pwd)
PYTHON_PATH=$(which python3)

# 建立 cron job 命令
CRON_JOB="0 9 * * 1 cd $CURRENT_DIR && $PYTHON_PATH manual_update.py >> tracker.log 2>&1"

# 檢查是否已經存在相同的 cron job
if crontab -l 2>/dev/null | grep -q "manual_update.py"; then
    echo "⚠️  發現已存在的 cron job，正在移除..."
    crontab -l 2>/dev/null | grep -v "manual_update.py" | crontab -
fi

# 新增新的 cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ cron job 設定完成！"
echo "📅 每週一上午 9:00 自動執行"
echo "📝 日誌檔案：tracker.log"
echo ""
echo "查看目前的 cron jobs："
crontab -l

echo ""
echo "💡 注意事項："
echo "- 電腦必須保持開機狀態"
echo "- 網路必須保持連線"
echo "- 如果要停止，執行：crontab -e 並刪除對應行" 