import plotly.express as px
import pandas as pd

# 1. 準備研究進度資料
data = [
    dict(Task="文獻探討與實驗設計籌備", Start='2026-01-01', Finish='2026-04-30', Phase="前期準備"),
    dict(Task="監測設備架設與程式測試", Start='2026-05-01', Finish='2026-05-31', Phase="前期準備"),
    dict(Task="實驗數據蒐集（環境/效率）", Start='2026-05-01', Finish='2026-06-30', Phase="實驗階段"),
    dict(Task="數據前處理與統計分析", Start='2026-06-01', Finish='2026-07-31', Phase="實驗階段"),
    dict(Task="預測模型建構與驗證", Start='2026-08-01', Finish='2026-09-30', Phase="報告撰寫"),
    dict(Task="撰寫研究結論", Start='2026-09-01', Finish='2026-09-30', Phase="報告撰寫"),
    dict(Task="撰寫研究報告與成果製作", Start='2026-10-01', Finish='2026-10-31', Phase="報告撰寫")
]
df = pd.DataFrame(data)

# 2. 建立甘特圖 
fig = px.timeline(
    df, 
    x_start="Start", 
    x_end="Finish", 
    y="Task", 
    color="Phase", 
    title="研究進度圖",
    labels={"Task": "", "Phase": "階段"} 
)

# ================= 新增多條垂直虛線 (里程碑) =================

# 1. 建立一個包含所有里程碑的清單 (可以在這裡隨意新增或修改)
milestones = [
    {"date": "2026-06-20", "text": "第一次期初研習營"},
    {"date": "2026-08-22", "text": "第二次期中研習營"},
    {"date": "2026-10-18", "text": "第三次期末研習營"}
]

# 2. 使用迴圈，把每一條線畫到圖表上
for ms in milestones:
    # 將日期字串轉換為 Plotly 支援的毫秒時間戳格式
    ms_timestamp = pd.Timestamp(ms["date"]).timestamp() * 1000
    
    fig.add_vline(
        x=ms_timestamp, 
        line_width=2, 
        line_dash="dash",   # 虛線樣式
        line_color="red",   # 線條顏色 (可以改成 "orange", "blue" 等)
        annotation_text=ms["text"], 
        annotation_position="top right"
    )

# =========================================================

# 3. 調整排版 (反轉 Y 軸讓第一個任務顯示在最上方，並放大左側文字)
fig.update_yaxes(
    autorange="reversed",
    tickfont=dict(size=16)  # 新增這行：設定 Y 軸的字體大小 (數字可自行調整)
)

# 統一放大整張圖表的所有基礎字體
fig.update_layout(font=dict(size=14))

# 4. 顯示圖表
fig.show()