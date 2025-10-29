import tkinter as tk
import random
import threading
import time

# 存储所有窗口实例，用于单个窗口关闭时清理
windows = []
# 存储窗口线程，便于管理
threads = []


def show_warm_tip():
    """创建并显示温馨提示窗口"""
    window = tk.Tk()
    windows.append(window)  # 记录窗口实例

    # 窗口位置随机（避免超出屏幕范围）
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width, window_height = 250, 60
    x = random.randrange(0, screen_width - window_width)
    y = random.randrange(0, screen_height - window_height)

    # 窗口基础设置
    window.title('温馨提示')
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    window.attributes('-topmost', True)  # 窗口置顶，确保能看到

    # 随机选择提示文字
    tips = [
        "多喝水哦~", "保持微笑呀", "每天都要元气满满",
        "记得吃水果", "保持好心情", "好好爱自己",
        "梦想成真", "别熬夜", "天冷了，多穿衣服", "今天过得开心吗"
    ]
    tip = random.choice(tips)

    # 随机选择背景色（已修正原错误颜色名 "honeyedew" 为 "honeydew"）
    bg_color = [
        "lightpink", "skyblue", "lightgreen", "lavender", "lightyellow",
        "plum", "coral", "bisque", "aquamarine", "mistyrose",
        "honeydew", "lavenderblush", "oldlace"
    ]
    bg = random.choice(bg_color)

    # 创建提示标签并显示
    tk.Label(
        window, text=tip, bg=bg,
        font=("微软雅黑", 16),
        width=30, height=3
    ).pack()

    # 单个窗口关闭时，从列表中移除实例（避免内存残留）
    def on_window_close():
        if window in windows:
            windows.remove(window)
        window.destroy()
    window.protocol("WM_DELETE_WINDOW", on_window_close)

    # 启动窗口消息循环
    window.mainloop()


if __name__ == "__main__":
    print("""
                    ____      
  ___  ___  ___/ / /___ __
 / _ \/ _ \/ _  / __/ // /
/_//_/_//_/\_,_/\__/\_, / 
                   /___/  """)
    try:
        # 循环创建300个窗口线程（间隔0.01秒，避免系统卡顿）
        for _ in range(300):
            t = threading.Thread(target=show_warm_tip)
            threads.append(t)
            t.start()
            time.sleep(0.01)

        # 等待所有线程执行完毕（窗口关闭后线程才会结束）
        for t in threads:
            t.join()
    except Exception as e:
        print(f"程序运行中出现小问题：{e}")