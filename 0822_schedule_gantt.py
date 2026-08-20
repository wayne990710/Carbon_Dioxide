import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

# 1. 建立專案任務資料
tasks_data = [
    # Phase 1: Midterm Workshop
    {
        "Phase": "Phase 1: Midterm Workshop",
        "Category": "Hardware & Tool Dev",
        "Task": "Sensor Deployment",
        "Start": "2026-03-01",
        "End": "2026-04-15",
        "Status": "Completed",
    },
    {
        "Phase": "Phase 1: Midterm Workshop",
        "Category": "Hardware & Tool Dev",
        "Task": "Stroop Platform",
        "Start": "2026-03-15",
        "End": "2026-05-01",
        "Status": "Completed",
    },
    {
        "Phase": "Phase 1: Midterm Workshop",
        "Category": "Hardware & Tool Dev",
        "Task": "Environ. Logging",
        "Start": "2026-04-15",
        "End": "2026-05-31",
        "Status": "Completed",
    },
    {
        "Phase": "Phase 1: Midterm Workshop",
        "Category": "REC Review",
        "Task": "REC Review",
        "Start": "2026-05-01",
        "End": "2026-08-25",
        "Status": "In Progress",
    },
    {
        "Phase": "Phase 1: Midterm Workshop",
        "Category": "REC Review",
        "Task": "Consent Protocols",
        "Start": "2026-05-15",
        "End": "2026-08-25",
        "Status": "In Progress",
    },
    {
        "Phase": "Phase 1: Midterm Workshop",
        "Category": "REC Review",
        "Task": "De-identification Setup",
        "Start": "2026-06-15",
        "End": "2026-08-25",
        "Status": "In Progress",
    },
    # Phase 2: Final Workshop
    {
        "Phase": "Phase 2: Final Workshop",
        "Category": "Data Collection",
        "Task": "Cohort Recruitment",
        "Start": "2026-08-25",
        "End": "2026-09-20",
        "Status": "Upcoming",
    },
    {
        "Phase": "Phase 2: Final Workshop",
        "Category": "Data Collection",
        "Task": "Synchronous Logging",
        "Start": "2026-09-15",
        "End": "2026-10-20",
        "Status": "Upcoming",
    },
    {
        "Phase": "Phase 2: Final Workshop",
        "Category": "Data Collection",
        "Task": "Feature Extraction",
        "Start": "2026-10-10",
        "End": "2026-11-15",
        "Status": "Upcoming",
    },
    # Phase 3: Taiwan International Science Fair (TISF Deliverables)
    {
        "Phase": "Phase 3: TISF Deliverables",
        "Category": "Synthesis & Modeling",
        "Task": "Model Training",
        "Start": "2026-11-01",
        "End": "2026-12-10",
        "Status": "Upcoming",
    },
    {
        "Phase": "Phase 3: TISF Deliverables",
        "Category": "Synthesis & Modeling",
        "Task": "Ventilation Protocol",
        "Start": "2026-11-20",
        "End": "2026-12-25",
        "Status": "Upcoming",
    },
    {
        "Phase": "Phase 3: TISF Deliverables",
        "Category": "Synthesis & Modeling",
        "Task": "Final Defense",
        "Start": "2026-12-15",
        "End": "2027-01-20",
        "Status": "Upcoming",
    },
]

# 2. 資料轉換與時間計算
df = pd.DataFrame(tasks_data)
df["Start"] = pd.to_datetime(df["Start"])
df["End"] = pd.to_datetime(df["End"])
df["Duration"] = (df["End"] - df["Start"]).dt.days

# 3. 繪圖設定與背景顏色配置
bg_color = "#f8fafc"
fig, ax = plt.subplots(figsize=(12, 7), facecolor=bg_color)
ax.set_facecolor(bg_color)

phase_colors = {
    "Phase 1: Midterm Workshop": "#2B5C8F",
    "Phase 2: Final Workshop": "#4A90E2",
    "Phase 3: TISF Deliverables": "#50B8B3",
}

# 繪製水平長條
for idx, row in df.iterrows():
    ax.barh(
        y=idx,
        width=row["Duration"],
        left=mdates.date2num(row["Start"]),
        height=0.55,
        color=phase_colors[row["Phase"]],
        alpha=0.9,
    )

# 4. 座標軸與標籤設定
ax.set_yticks(range(len(df)))
ax.set_yticklabels(df["Task"], fontsize=10)
ax.invert_yaxis()

ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=0, fontsize=10)

# 格線與外框線顏色適配
ax.grid(axis="x", linestyle="--", alpha=0.5, color="#cbd5e1")
ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_color("#cbd5e1")

# 5. 圖例設定（右上角與相應底色）
legend_elements = [
    plt.Rectangle((0, 0), 1, 1, color=color, label=phase)
    for phase, color in phase_colors.items()
]
ax.legend(
    handles=legend_elements,
    loc="upper right",
    frameon=True,
    fontsize=9,
    title="Research Phases",
    facecolor=bg_color,
    edgecolor="#cbd5e1",
)

plt.title("Research Progress & Timeline", fontsize=14, weight="bold", pad=15)
plt.tight_layout()

# 儲存圖片時保留指定背景色
plt.savefig("research_timeline_gantt.png", dpi=300, facecolor=bg_color)
plt.show()