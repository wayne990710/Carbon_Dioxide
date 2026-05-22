import tkinter as tk
import random
import time
from datetime import datetime
import csv
import os

class StroopTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Stroop Test")
        self.root.geometry("900x700") 
        self.root.configure(bg="#f8f9fa")
        
        # 對應關係：keysym -> (文字意義, 顯示顏色, 字體顏色)
        self.color_map = {
            "f": ("紅色", "#e74c3c", "white"),       
            "Alt_L": ("綠色", "#2ecc71", "white"),   
            "space": ("藍色", "#3498db", "white"),   
            "j": ("黃色", "#f1c40f", "black")        
        }
        self.color_keys = list(self.color_map.keys())
        
        self.total_trials = 24  
        self.current_trial = 0
        self.results = []
        self.start_time = 0
        self.is_waiting = False
        
        self.phase = "intro"
        self.practice_idx = 0
        self.practice_trials = []
        self.real_test_conditions = []

        self.setup_ui()

    def setup_ui(self):
        # 1. 頂部：指導語
        self.instruction_label = tk.Label(self.root, text=(
            "【重要】請確認鍵盤已切換至「英文輸入模式」\n\n"
            "請根據文字或色塊的「顏色」按下對應按鍵，忽略文字本身的意義。\n\n"
            f"本次正式測驗共計 {self.total_trials} 題，過程大約只需 40 秒。\n"
            "我們將先進行 8 題練習，準備好請點擊下方按鈕開始。"
        ), font=("微軟正黑體", 14), bg="#f8f9fa", fg="#333333")
        self.instruction_label.pack(side=tk.TOP, pady=15)

        # 2. 頂部偏中：動態進度提示標籤
        self.progress_label = tk.Label(self.root, text="", font=("微軟正黑體", 18, "bold"), bg="#f8f9fa", fg="#2c3e50")
        self.progress_label.pack(side=tk.TOP, pady=5)

        # 3. 底部：視覺化小鍵盤區塊
        self.keyboard_frame = self.create_mini_keyboard(self.root)
        self.keyboard_frame.pack(side=tk.BOTTOM, pady=30)

        # 4. 中下方：建立一個容器放按鈕與回饋提示文字
        self.action_frame = tk.Frame(self.root, bg="#f8f9fa")
        self.action_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.action_button = tk.Button(self.action_frame, text="開始練習 (點擊或按空白鍵即可開始)", font=("微軟正黑體", 14), command=self.start_practice)
        self.action_button.pack(pady=5)

        self.hint_label = tk.Label(self.action_frame, text="", font=("微軟正黑體", 16), bg="#f8f9fa", fg="gray")
        self.hint_label.pack(pady=5)

        # 5. 中間：測驗文字顯示區
        self.word_label = tk.Label(self.root, text="", font=("微軟正黑體", 80, "bold"), bg="#f8f9fa")
        self.word_label.pack(expand=True)

        self.root.bind("<Key>", self.handle_keypress)

    def create_mini_keyboard(self, parent):
        kbd_frame = tk.Frame(parent, bg="#dcdcdc", padx=15, pady=15, relief="flat", bd=0)
        
        layout = [
            [("A", 4, None), ("S", 4, None), ("D", 4, None), ("F\n(紅)", 4, "f"), ("G", 4, None), 
             ("H", 4, None), ("J\n(黃)", 4, "j"), ("K", 4, None), ("L", 4, None)],
            [("Z", 4, None), ("X", 4, None), ("C", 4, None), ("V", 4, None), 
             ("B", 4, None), ("N", 4, None), ("M", 4, None)],
            [("Ctrl", 5, None), ("Win", 5, None), ("Alt\n(綠)", 5, "Alt_L"), 
             ("Space\n(藍)", 18, "space"), ("Alt", 5, None), ("Ctrl", 5, None)]
        ]
        
        for i, row in enumerate(layout):
            row_frame = tk.Frame(kbd_frame, bg="#dcdcdc")
            if i == 1:
                row_frame.pack(side=tk.TOP, pady=3, padx=(20, 0))
            elif i == 2:
                row_frame.pack(side=tk.TOP, pady=3, padx=(10, 0))
            else:
                row_frame.pack(side=tk.TOP, pady=3)
            
            for key_text, width, key_id in row:
                bg_color = "#ffffff"
                fg_color = "#555555"
                font_weight = "normal"
                relief = "raised"
                
                if key_id and key_id in self.color_map:
                    _, bg_color, fg_color = self.color_map[key_id]
                    font_weight = "bold"
                    relief = "ridge"
                
                lbl = tk.Label(row_frame, text=key_text, width=width, height=2, 
                               bg=bg_color, fg=fg_color, font=("Arial", 11, font_weight),
                               relief=relief, bd=3)
                lbl.pack(side=tk.LEFT, padx=3)
                
        return kbd_frame

    def start_practice(self):
        self.phase = "practice"
        self.action_button.pack_forget()
        self.instruction_label.config(text="請根據顯示的「顏色」按下對應按鍵，忽略文字本身的意義。")
        self.practice_idx = 0
        
        self.practice_trials = []
        
        first_4_colors = list(self.color_keys)
        random.shuffle(first_4_colors)
        for color_key in first_4_colors:
            self.practice_trials.append({
                "target_color_key": color_key,
                "word_meaning_key": random.choice(self.color_keys)
            })
            
        last_4_colors = list(self.color_keys)
        random.shuffle(last_4_colors)
        for color_key in last_4_colors:
            available_words = [k for k in self.color_keys if k != color_key]
            self.practice_trials.append({
                "target_color_key": color_key,
                "word_meaning_key": random.choice(available_words)
            })

        self.root.focus_set()
        self.next_practice_trial()

    def show_fixation_cross(self, callback):
        self.is_waiting = True
        self.word_label.config(text="+", fg="black", font=("微軟正黑體", 50))
        self.root.after(500, callback)

    def next_practice_trial(self):
        if self.practice_idx < 8:
            self.show_fixation_cross(self.show_practice_stimulus)
        else:
            self.phase = "practice_done"
            self.progress_label.config(text="") 
            self.word_label.config(text="練習結束", fg="black", font=("微軟正黑體", 40))
            self.hint_label.config(text=f"即將進入正式測驗（共 {self.total_trials} 題）。")
            self.action_button.config(text="開始正式測驗 (點擊或按空白鍵即可開始)", command=self.prepare_real_test)
            self.action_button.pack(pady=10)

    def show_practice_stimulus(self):
        self.is_waiting = False
        self.progress_label.config(text=f"【 練 習 題 {self.practice_idx + 1} / 8 】")

        trial_data = self.practice_trials[self.practice_idx]
        target_key = trial_data["target_color_key"]
        word_key = trial_data["word_meaning_key"]
        
        self.current_word = self.color_map[word_key][0]
        self.current_color = self.color_map[target_key][1]
        self.correct_key = target_key
        
        self.word_label.config(text=self.current_word, fg=self.current_color, font=("微軟正黑體", 80, "bold"))
        self.hint_label.config(text="") 
        self.start_time = time.time()

    def prepare_real_test(self):
        self.phase = "countdown"
        self.action_button.pack_forget()
        self.hint_label.config(text="") 
        self.progress_label.config(text="") 
        self.instruction_label.config(text="請根據顯示的「顏色」按下對應按鍵，忽略文字本身的意義。")
        self.current_trial = 0
        self.results = []
        
        self.real_test_conditions = ["中性"] * 8 + ["一致"] * 8 + ["不一致"] * 8
        random.shuffle(self.real_test_conditions)

        self.root.focus_set()
        self.is_waiting = True 
        
        self.countdown(3)

    def countdown(self, count):
        if count > 0:
            self.word_label.config(text=str(count), fg="black", font=("微軟正黑體", 80, "bold"))
            self.root.after(1000, self.countdown, count - 1)
        else:
            self.phase = "testing"
            self.word_label.config(text="")
            self.root.after(500, self.next_trial)

    def next_trial(self):
        if self.current_trial < self.total_trials:
            self.show_fixation_cross(self.show_real_stimulus)
        else:
            self.phase = "done"
            self.show_results()

    def show_real_stimulus(self):
        self.is_waiting = False
        
        self.progress_label.config(text=f"第 {self.current_trial + 1} 題，共 {self.total_trials} 題")
        
        self.condition = self.real_test_conditions[self.current_trial]
        color_key = random.choice(self.color_keys)
        self.current_color = self.color_map[color_key][1]
        self.correct_key = color_key
        
        if self.condition == "中性":
            self.current_word = "███"
        elif self.condition == "一致":
            self.current_word = self.color_map[color_key][0]
        else: 
            available_words = [k for k in self.color_keys if k != color_key]
            word_key = random.choice(available_words)
            self.current_word = self.color_map[word_key][0]
            
        self.word_label.config(text=self.current_word, fg=self.current_color, font=("微軟正黑體", 80, "bold"))
        self.start_time = time.time()

    def handle_keypress(self, event):
        pressed_key = event.keysym
        if pressed_key in ["F", "J"]:
            pressed_key = pressed_key.lower()

        if pressed_key == "space":
            if self.phase == "intro":
                self.start_practice()
                return "break"
            elif self.phase == "practice_done":
                self.prepare_real_test()
                return "break"

        if self.is_waiting:
            return

        if self.phase == "practice" and self.start_time > 0 and self.practice_idx < 8:
            if pressed_key in self.color_keys:
                if pressed_key == self.correct_key:
                    self.practice_idx += 1
                    self.is_waiting = True
                    self.word_label.config(text="")
                    self.hint_label.config(text="正確！", fg="green")
                    self.root.after(500, self.next_practice_trial)
                else:
                    self.hint_label.config(text=f"按錯囉！請參考下方鍵盤圖示", fg="red")
        
        elif self.phase == "testing" and self.current_trial < self.total_trials and self.start_time > 0:
            if pressed_key in self.color_keys:
                reaction_time = int((time.time() - self.start_time) * 1000)
                is_correct = (pressed_key == self.correct_key)
                
                self.results.append({
                    "trial": self.current_trial + 1,
                    "condition": self.condition,
                    "rt": reaction_time,
                    "correct": is_correct
                })
                
                self.current_trial += 1
                self.is_waiting = True
                
                self.word_label.config(text="")
                self.root.after(300, self.next_trial)
        
        if pressed_key == "Alt_L":
            return "break"

    def show_results(self):
        self.progress_label.config(text="") 
        self.instruction_label.config(text="")
        self.word_label.config(text="測驗結束", fg="black", font=("微軟正黑體", 50, "bold"))
        # 提示文字更新為已匯出資料
        self.hint_label.config(text="測驗完成！資料已自動匯出為 CSV 報表。", fg="#2c3e50")
        
        correct_count = sum(1 for r in self.results if r["correct"])
        accuracy = (correct_count / self.total_trials) * 100
        
        rt_neutral = [r["rt"] for r in self.results if r["condition"] == "中性" and r["correct"]]
        rt_congruent = [r["rt"] for r in self.results if r["condition"] == "一致" and r["correct"]]
        rt_incongruent = [r["rt"] for r in self.results if r["condition"] == "不一致" and r["correct"]]
        
        avg_neutral = sum(rt_neutral) / len(rt_neutral) if rt_neutral else 0
        avg_congruent = sum(rt_congruent) / len(rt_congruent) if rt_congruent else 0
        avg_incongruent = sum(rt_incongruent) / len(rt_incongruent) if rt_incongruent else 0
        
        interference_score = avg_incongruent - avg_neutral

        # =========================================================
        # 自動匯出分析用 CSV 檔案 (新增部分)
        # =========================================================
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        readable_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 1. 匯出每題詳細原始資料：供檢視單次測驗的每一題狀況
        detail_filename = os.path.join("output", f"stroop_detail_{timestamp_str}.csv")
        # 使用 utf-8-sig 確保用 Excel 開啟時中文不會亂碼
        with open(detail_filename, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(["測驗時間", "題號", "情境", "反應時間(ms)", "是否正確"])
            for r in self.results:
                writer.writerow([readable_time, r['trial'], r['condition'], r['rt'], "是" if r['correct'] else "否"])

        # 2. 寫入總體摘要資料庫：適合長期累積多名受試者或多次的成績
        summary_filename = os.path.join("output", "stroop_summary_database.csv")
        file_exists = os.path.isfile(summary_filename)
        with open(summary_filename, mode='a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            if not file_exists:
                # 檔案不存在時先寫入標題列
                writer.writerow(["測驗時間", "總題數", "正確率(%)", "中性情境平均(ms)", "一致情境平均(ms)", "不一致情境平均(ms)", "Stroop干擾分數(ms)"])
            writer.writerow([
                readable_time,
                self.total_trials,
                round(accuracy, 1),
                round(avg_neutral, 0),
                round(avg_congruent, 0),
                round(avg_incongruent, 0),
                round(interference_score, 0)
            ])
            
        print(f"\n✅ 【資料已自動儲存至程式所在資料夾】")
        print(f"1. 單次詳細記錄：{detail_filename}")
        print(f"2. 總體成績資料庫：{summary_filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StroopTest(root)
    root.mainloop()