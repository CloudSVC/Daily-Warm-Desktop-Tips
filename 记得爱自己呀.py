import tkinter as tk
import random
import sys

# 全局控制：存储所有子窗口实例、窗口创建计数
child_windows = []
created_window_count = 0
total_target = 300  # 提示窗总数


def close_all_windows(main_window):
    """关闭所有子窗口 + 主窗口，彻底退出程序"""
    # 先关闭所有温馨提示窗和结束提示窗
    for win in child_windows[:]:
        try:
            win.destroy()
            child_windows.remove(win)
        except Exception as e:
            print(f"清理窗口忽略小问题：{e}")
    # 关闭隐藏的主窗口，终止主循环
    main_window.destroy()
    sys.exit(0)


def create_warm_tip_window(main_window):
    """在主线程创建单个温馨提示窗（Tkinter安全操作）"""
    global created_window_count

    # 若已创建足够数量的窗口，停止创建
    if created_window_count >= total_target:
        return

    # 1. 创建温馨提示子窗口
    win = tk.Toplevel(main_window)  # 用Toplevel，依赖主窗口，避免多主循环
    child_windows.append(win)
    created_window_count += 1

    # 2. 窗口位置随机（避免超出屏幕）
    screen_w = main_window.winfo_screenwidth()
    screen_h = main_window.winfo_screenheight()
    win_w, win_h = 250, 60
    x = random.randrange(0, screen_w - win_w)
    y = random.randrange(0, screen_h - win_h)
    win.geometry(f"{win_w}x{win_h}+{x}+{y}")

    # 3. 窗口样式设置
    win.title("温馨提示")
    win.attributes("-topmost", True)  # 置顶显示

    # 4. 随机文案和背景色
    tips = [
        "多喝水哦~", "保持微笑呀", "每天都要元气满满",
        "记得吃水果", "保持好心情", "好好爱自己",
        "梦想成真", "别熬夜", "天冷了，多穿衣服", "今天过得开心吗"
    ]
    bg_colors = [
        "lightpink", "skyblue", "lightgreen", "lavender", "lightyellow",
        "plum", "coral", "bisque", "aquamarine", "mistyrose",
        "honeydew", "lavenderblush", "oldlace"
    ]
    tk.Label(
        win, text=random.choice(tips),
        bg=random.choice(bg_colors),
        font=("微软雅黑", 16),
        width=30, height=3
    ).pack()

    def on_child_close():
        if win in child_windows:
            child_windows.remove(win)
        win.destroy()
    win.protocol("WM_DELETE_WINDOW", on_child_close)

    # 定时创建下一个窗口（主线程定时，间隔10ms，避免卡顿）
    if created_window_count < total_target:
        main_window.after(100, create_warm_tip_window, main_window)
    else:
        show_end_tip(main_window)


def show_end_tip(main_window):
    """在主线程创建结束提示窗（5秒后自动退出）"""
    # 1. 创建结束提示子窗口（居中显示）
    end_win = tk.Toplevel(main_window)
    child_windows.append(end_win)
    screen_w = main_window.winfo_screenwidth()
    screen_h = main_window.winfo_screenheight()
    win_w, win_h = 350, 90
    x = int((screen_w - win_w) / 2)
    y = int((screen_h - win_h) / 2)
    end_win.geometry(f"{win_w}x{win_h}+{x}+{y}")

    end_win.title("5秒后程序自动退出")
    end_win.attributes("-topmost", True)
    bg = random.choice([
        "lightpink", "skyblue", "lightgreen", "lavender", "lightyellow"
    ])
    tk.Label(
        end_win, text="要天天开心哦~~~",
        bg=bg, font=("微软雅黑", 16),
        width=30, height=3
    ).pack()

    def on_end_close():
        close_all_windows(main_window)
    end_win.protocol("WM_DELETE_WINDOW", on_end_close)

    # 5秒后自动退出（主线程定时，安全触发）
    main_window.after(5000, close_all_windows, main_window)


if __name__ == "__main__":
    print("""
                ____      
  ___  ___  ___/ / /___ __
 / _ \/ _ \/ _  / __/ // /
/_//_/_//_/\_,_/\__/\_, / 
                   /___/   
    """)

    # 创建1个主窗口（隐藏，作为所有子窗口的父容器）
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口，只用于管理子窗口和主循环

    # 启动主线程定时任务：创建第一个温馨提示窗
    root.after(100, create_warm_tip_window, root)

    # 启动Tkinter主循环（所有GUI操作都在这个主线程循环中执行）
    root.mainloop()