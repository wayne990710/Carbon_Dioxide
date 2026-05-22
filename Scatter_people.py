import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import csv
import numpy as np
from scipy.ndimage import gaussian_filter1d

def convert_excel_time(time_str):
    """
    自動判斷並將 Excel 的小數時間轉換為 HH:MM:SS 字串
    """
    try:
        time_float = float(time_str)
        time_fraction = time_float % 1
        total_seconds = int(round(time_fraction * 86400))
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    except ValueError:
        return time_str

def plot_multiple_co2_charts(datasets, output_filename="CO2_people.png"):
    """
    接收多筆數據的設定，並繪製在同一張 1920x1080 的圖表上進行比較
    X 軸改為顯示經過的「分鐘數」(0~30)
    """
    # 解決 Matplotlib 中文顯示問題
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'PingFang HK', 'Taipei Sans TC Beta', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False 

    # 設定寬 19.2 吋、高 10.8 吋，搭配 dpi=100，產出即為 1920 x 1080 畫素
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)

    # 依序處理每一筆設定好的資料
    for data_info in datasets:
        file_path = data_info['file']
        label_name = data_info['label']
        line_color = data_info['color']
        
        time_list = []
        co2_list = []

        # ================= 1. 讀取 CSV 檔案並自動轉換時間 =================
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 2:
                        time_val = row[0].strip()
                        co2_val = row[1].strip()
                        if time_val and co2_val:
                            try:
                                co2_float = float(co2_val)
                                clean_time_str = convert_excel_time(time_val)
                                time_list.append(clean_time_str)
                                co2_list.append(co2_float)
                            except ValueError:
                                continue
        except FileNotFoundError:
            print(f"錯誤：找不到檔案「{file_path}」，已略過此筆資料。")
            continue
        except Exception as e:
            print(f"讀取「{file_path}」時發生錯誤：{e}")
            continue

        if not time_list:
            print(f"警告：檔案「{file_path}」無有效資料。")
            continue

        # ================= 2. 將時間轉換為「經過分鐘數」 =================
        elapsed_minutes = []
        first_time_obj = None
        base_date = datetime(2026, 1, 1) # 用一個固定的日期作為計算基準
        
        for t_str in time_list:
            try:
                # 讀取時間並結合基準日期
                time_obj = datetime.strptime(t_str, "%H:%M:%S").time()
                dt_obj = datetime.combine(base_date, time_obj)
                
                # 記錄這筆資料的第一個時間點當作起點 (t=0)
                if first_time_obj is None:
                    first_time_obj = dt_obj
                
                # 處理可能的跨夜問題 (例如從 23:59 錄到 00:05)
                time_diff = dt_obj - first_time_obj
                if time_diff.total_seconds() < 0:
                    dt_obj += timedelta(days=1)
                    time_diff = dt_obj - first_time_obj
                
                # 換算成經過的分鐘數
                mins = time_diff.total_seconds() / 60.0
                elapsed_minutes.append(mins)
                
            except ValueError:
                continue

        # 確保資料依照經過時間排序
        sorted_data = sorted(zip(elapsed_minutes, co2_list), key=lambda x: x[0])
        sorted_mins = [data[0] for data in sorted_data]
        sorted_co2 = [data[1] for data in sorted_data]

        # ================= 3. 建立連續時間軸與插值 (改用分鐘數) =================
        continuous_mins = np.linspace(min(sorted_mins), max(sorted_mins), num=1000)
        continuous_co2 = np.interp(continuous_mins, sorted_mins, sorted_co2)
        smoothed_co2 = gaussian_filter1d(continuous_co2, sigma=15)

        # ================= 4. 將該筆資料畫上圖表 =================
        # 散佈點不加 label，保持圖例乾淨
        ax.scatter(sorted_mins, sorted_co2, color=line_color, s=20, alpha=0.3)
        # 趨勢線加粗並保留 label 屬性（即使不顯示圖例，底層屬性仍可保留）
        ax.plot(continuous_mins, smoothed_co2, color=line_color, linewidth=4.0, label=label_name)

    # ================= 5. 圖表整體版面設定 =================
    # 【已刪除圖例設定】： ax.legend(fontsize=20, loc='upper left')

    # 鎖定 X 軸範圍為 0 到 30
    ax.set_xlim(0, 30)
    
    # 讓 X 軸每隔 5 分鐘顯示一個刻度 (0, 5, 10, 15, 20, 25, 30)
    ax.set_xticks(np.arange(0, 35, 5))

    plt.title("人數與二氧化碳濃度關係圖", fontsize=32, pad=25)
    
    # X 軸標題改為「經過時間（分鐘）」
    plt.xlabel("經過時間（分鐘）", fontsize=24, labelpad=15)
    plt.ylabel("二氧化碳（ppm）", fontsize=24, labelpad=15)
    
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    # ================= 6. 輸出與顯示 =================
    plt.savefig(output_filename, dpi=100)
    print(f"圖表已存檔為：{output_filename} (尺寸: 1920x1080 pixels)")
    
    plt.show()

# ================= 測試區塊 =================
if __name__ == "__main__":
    my_datasets = [
        {"file": "20260206_ClassBegin.csv", "label": "2/6 上課", "color": "#1f77b4"},
        {"file": "20260206_ClassEnd.csv", "label": "2/6 下課", "color": "#ff7f0e"}
    ]
    
    plot_multiple_co2_charts(my_datasets, output_filename="CO2_people.png")