import json
import random
import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime

with open('vocab.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

num_entries = len(data)
auto_answer = False

def check_answer(user_choice):
    global question_count, score, wrong_answers, random_entry, word, chinese_translation, part_of_speech
    if question_count < total_questions:
        correct_answer = options.index(random_entry)
        if user_choice == correct_answer:
            score += 1
            result_label.config(text=f"正確答案！ {chinese_translation} {word} ({part_of_speech}.) 目前分數:{score}", fg='green')
        else:
            result_label.config(text=f"答案錯誤，正確答案是選項 {correct_answer}: {chinese_translation} {word} ({part_of_speech}.) 目前分數:{score}", fg='red')
            wrong_answers.append((chinese_translation, word, part_of_speech))
        
        # 打印所选的答案和正确答案
        print(f"所选答案: {user_choice}, 正确答案: {correct_answer}")
        
        question_count += 1
        if question_count < total_questions:
            next_question()
        else:
            show_final_score()

def next_question():
    global random_entry, word, chinese_translation, part_of_speech, options
    random_entry = random.choice(data)
    word = random_entry["word"]
    chinese_translation = random_entry["chinese"]
    part_of_speech = random_entry["partOfSpeech"]
    options = [random.choice(data) for _ in range(3)]
    options.append(random_entry)
    random.shuffle(options)

    if quiz_type == "1":
        question_label.config(text=f"英文：{word} ({part_of_speech}.) ({question_count + 1}/{total_questions})")
    else:
        question_label.config(text=f"中文：{chinese_translation} ({part_of_speech}.) ({question_count + 1}/{total_questions})")

    for i, option in enumerate(options, start=1):
        if quiz_type == "1":
            option_buttons[i - 1].config(text=f"{i}. {option['chinese']}")
            if auto_answer:  # Automatically select the correct answer
                window.after(1000, lambda i=i: check_answer(i - 1))
        else:
            option_buttons[i - 1].config(text=f"{i}. {option['word']}")
            if auto_answer:  # Automatically select the correct answer
                window.after(1000, lambda i=i: check_answer(i - 1))
    result_label.config(text="", fg='black')

def show_final_score():
    global quiz_finished
    quiz_finished = True  # 设置为True表示测验结束
    global wrong_answers
    percent_score = score * (100 / total_questions)
    result_label.config(text=f"試題結束! 作答成績: {round(float(percent_score))}%", fg='black')

    # 创建错误列表的标题标签
    wrong_answers_title_label = tk.Label(window, text="錯誤答案列表：", font=("Helvetica", 14))
    wrong_answers_title_label.pack()
    
    if len(wrong_answers) > 0:
        split_index = len(wrong_answers) // 2
        wrong_answers_part1 = "\n".join([f"{answer[0]} {answer[1]} ({answer[2]}.)" for answer in wrong_answers[:split_index]])
        wrong_answers_part2 = "\n".join([f"{answer[0]} {answer[1]} ({answer[2]}.)" for answer in wrong_answers[split_index:]])
        
        # 创建两个标签来显示左右两列的错误答案
        wrong_answers_label1 = tk.Label(window, text=wrong_answers_part1, font=("Helvetica", 12), justify='left')
        wrong_answers_label2 = tk.Label(window, text=wrong_answers_part2, font=("Helvetica", 12), justify='left')
        
        # 将这两个标签放置在窗口中，一列在左侧，一列在右侧
        wrong_answers_label1.pack(side='left', padx=10)
        wrong_answers_label2.pack(side='right', padx=10)
        
    else:
        wrong_answers_label.config(text="恭喜！沒有錯誤答案。")
    wrong_answers_label.pack()

    # 保存分数到 score.json 文件
    save_score()

# Create a Tkinter window.
window = tk.Tk()
window.title("單字詞彙測驗系統")

# Create GUI elements.
question_label = tk.Label(window, text="", font=("Helvetica", 16))
result_label = tk.Label(window, text="", font=("Helvetica", 14))
option_buttons = []

for i in range(4):
    option_button = tk.Button(window, text="", font=("Helvetica", 12), command=lambda i=i: check_answer(i))
    option_buttons.append(option_button)

# Initialize quiz variables.
quiz_type = None
total_questions = 0
question_count = 0
score = 0
wrong_answers = []
random_entry = None
word = ""
chinese_translation = ""
part_of_speech = ""
options = []
# 创建一个 Tkinter 变量，用于控制保存分数的开关状态
save_score_var = tk.BooleanVar()
save_score_var.set(True)  # 默认设置为保存分数

# 创建保存分数的 Checkbutton
save_score_checkbox = tk.Checkbutton(window, text="保存分数", variable=save_score_var, font=("Helvetica", 12))
save_score_checkbox.pack()

# 初始化开始时间
start_time = None

def save_score():
    # 获取当前日期和时间
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # 计算测试总时间
    end_time = time.time()
    total_time = round(end_time - start_time)

    # 构建分数信息字典
    score_info = {
        "date": date_time,
        "time": f"{total_time} 秒",
        "qs": total_questions,
        "score": score
    }

    # 读取已保存的分数数据
    try:
        with open('score.json', 'r', encoding='utf-8') as score_file:
            scores = json.load(score_file)
    except FileNotFoundError:
        scores = []

    # 添加当前分数信息到列表
    scores.append(score_info)

    # 写入更新后的分数数据到 score.json 文件
    with open('score.json', 'w', encoding='utf-8') as score_file:
        json.dump(scores, score_file, ensure_ascii=False, indent=4)

def show_final_score():
    global quiz_finished
    quiz_finished = True  # 设置为True表示测验结束
    global wrong_answers
    percent_score = score * (100 / total_questions)
    result_label.config(text=f"試題結束! 作答成績: {round(float(percent_score))}%", fg='black')

    # 创建错误列表的标题标签
    wrong_answers_title_label = tk.Label(window, text="錯誤答案列表：", font=("Helvetica", 14))
    wrong_answers_title_label.pack()
    
    if len(wrong_answers) > 0:
        split_index = len(wrong_answers) // 2
        wrong_answers_part1 = "\n".join([f"{answer[0]} {answer[1]} ({answer[2]}.)" for answer in wrong_answers[:split_index]])
        wrong_answers_part2 = "\n".join([f"{answer[0]} {answer[1]} ({answer[2]}.)" for answer in wrong_answers[split_index:]])
        
        # 创建两个标签来显示左右两列的错误答案
        wrong_answers_label1 = tk.Label(window, text=wrong_answers_part1, font=("Helvetica", 12), justify='left')
        wrong_answers_label2 = tk.Label(window, text=wrong_answers_part2, font=("Helvetica", 12), justify='left')
        
        # 将这两个标签放置在窗口中，一列在左侧，一列在右侧
        wrong_answers_label1.pack(side='left', padx=10)
        wrong_answers_label2.pack(side='right', padx=10)
        
    else:
        wrong_answers_label.config(text="恭喜！沒有錯誤答案。")
    wrong_answers_label.pack()

    # 根据保存分数的开关状态来保存分数
    if save_score_var.get():
        save_score()

def start_quiz():
    global quiz_type, total_questions, question_count, score, wrong_answers, start_time
    quiz_type = quiz_type_var.get()
    total_questions = int(total_questions_entry.get())
    question_count = 0
    score = 0
    wrong_answers = []
    start_time = time.time()  # 记录开始时间
    next_question()
    wrong_answers_label.pack_forget()

def restart_quiz():
    global question_count, score, wrong_answers
    question_count = 0
    score = 0
    wrong_answers = []
    next_question()
    wrong_answers_label.pack_forget()

# Layout GUI elements.
question_label.pack(pady=20)
for option_button in option_buttons:
    option_button.pack(pady=10)
result_label.pack(pady=10)

start_button_frame = tk.Frame(window)
quiz_type_label = tk.Label(start_button_frame, text="選擇測驗類型：", font=("Helvetica", 12))
quiz_type_var = tk.StringVar(value="1")
quiz_type_radio1 = tk.Radiobutton(start_button_frame, text="英文到中文", variable=quiz_type_var, value="1", font=("Helvetica", 12))
quiz_type_radio2 = tk.Radiobutton(start_button_frame, text="中文到英文", variable=quiz_type_var, value="2", font=("Helvetica", 12))
total_questions_label = tk.Label(start_button_frame, text="請輸入總題數：", font=("Helvetica", 12))
total_questions_entry = tk.Entry(start_button_frame, font=("Helvetica", 12))
start_button = tk.Button(start_button_frame, text="開始測驗", font=("Helvetica", 14), command=start_quiz)

quiz_type_label.grid(row=0, column=0, sticky='w')
quiz_type_radio1.grid(row=0, column=1)
quiz_type_radio2.grid(row=0, column=2)
total_questions_label.grid(row=1, column=0, sticky='w')
total_questions_entry.grid(row=1, column=1)
start_button.grid(row=2, column=0, columnspan=3, pady=10)

start_button_frame.pack(pady=20)

# Create a label for wrong answers but hide it initially.
wrong_answers_label = tk.Label(window, text="", font=("Helvetica", 12))
wrong_answers_label.pack()
wrong_answers_label.pack_forget()

# Start the Tkinter main loop.
window.mainloop()