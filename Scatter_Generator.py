import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import csv
from scipy.ndimage import gaussian_filter1d

def convert_excel_time(time_str):
    """
    自動判斷並將 Excel 的小數時間（如 0.37505787）轉換為 HH:MM:SS 字串
    """
    try:
        # 嘗試將字串轉為浮點數
        time_float = float(time_str)
        # 如果數字小於 1，代表它是 Excel 的時間比例
        # 取小數點部分 (以防有帶日期的數字)
        time_fraction = time_float % 1
        
        # 換算成一天中的總秒數 (一天有 86400 秒)
        total_seconds = int(round(time_fraction * 86400))
        
        # 計算出時、分、秒
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # 組合回 HH:MM:SS 的字串格式
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    except ValueError:
        # 如果無法轉為浮點數（例如本來就是 "09:00:05" 字串），就直接原封不動回傳
        return time_str

def plot_co2_chart_from_csv(file_path):
    """
    從 CSV 檔案讀取數據，繪製二氧化碳濃度圖表（數據點與平滑曲線共存，X軸僅顯示整點）
    :param file_path: CSV 檔案路徑
    """
    # 解決 Matplotlib 中文顯示問題
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'PingFang HK', 'Taipei Sans TC Beta', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False 

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
                            # 【重點修改】：呼叫轉換函式，處理 Excel 的小數時間
                            clean_time_str = convert_excel_time(time_val)
                            
                            time_list.append(clean_time_str)
                            co2_list.append(co2_float)
                        except ValueError:
                            # 略過標題行或無法解析為數字的 CO2 濃度
                            continue
    except FileNotFoundError:
        print(f"錯誤：找不到檔案「{file_path}」，請確認檔案路徑。")
        return
    except Exception as e:
        print(f"讀取檔案時發生錯誤：{e}")
        return

    if not time_list:
        print("警告：無法讀取有效的資料，請檢查 CSV 檔案格式！")
        return

    # ================= 2. 處理時間與排序 =================
    parsed_dates = []
    for t_str in time_list:
        try:
            dt = datetime.strptime(t_str, "%H:%M:%S")
            parsed_dates.append(dt)
        except ValueError:
            print(f"時間格式錯誤：{t_str}，請確保格式為 HH:MM:SS")
            return

    sorted_data = sorted(zip(parsed_dates, co2_list), key=lambda x: x[0])
    sorted_dates = [data[0] for data in sorted_data]
    sorted_co2 = [data[1] for data in sorted_data]

    # ================= 3. 開始繪製圖表 =================
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.scatter(sorted_dates, sorted_co2, color='#1f77b4', s=15, alpha=0.4, label='實際數據點')

    smoothed_co2 = gaussian_filter1d(sorted_co2, sigma=4)
    ax.plot(sorted_dates, smoothed_co2, color='#ff7f0e', linewidth=2.5, label='平滑趨勢線')

    ax.legend(fontsize=12, loc='upper left')

    ax.xaxis.set_major_locator(mdates.HourLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:00'))

    plt.title("114B 班教室二氧化碳濃度_20260106", fontsize=16, pad=15)
    plt.xlabel("時間", fontsize=12, labelpad=10)
    plt.ylabel("二氧化碳（ppm）", fontsize=12, labelpad=10)

    plt.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()

# ================= 測試區塊 =================
if __name__ == "__main__":
    csv_file_name = "Data_20260106.csv"
    plot_co2_chart_from_csv(csv_file_name)