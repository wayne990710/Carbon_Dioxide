import matplotlib.pyplot as plt

# --- 新增的字體設定區塊 ---
# 告訴 matplotlib 依序尋找微軟正黑體 (Windows) 或蘋方體 (Mac)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'PingFang TC', 'sans-serif']
# 確保圖表中的負號 (-) 也能正常顯示，不會變成方塊
plt.rcParams['axes.unicode_minus'] = False 
# ---------------------------

# 1. 準備已計算好的統計數據
stats = [
    {
        'label': '平日',
        'med': 733,
        'q1': 663,
        'q3': 861,
        'whislo': 366,
        'whishi': 1158,
        'fliers': []
    },
    {
        'label': '假日',
        'med': 765,
        'q1': 761,
        'q3': 769,
        'whislo': 749,
        'whishi': 781,
        'fliers': [819, 788, 707, 791]
    }
]

# 2. 設定圖表大小
fig, ax = plt.subplots(figsize=(8, 6))

# 3. 使用 bxp 繪製預先計算好數值的箱型圖
ax.bxp(stats, showfliers=True, patch_artist=True)

# 4. 加上標題與軸標籤
plt.title('114B 班教室二氧化碳濃度平日假日變化幅度比較圖', fontsize=15)
plt.xlabel('', fontsize=12)
plt.ylabel('二氧化碳濃度（ppm）', fontsize=12)

# 5. 顯示圖表
plt.show()