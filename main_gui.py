import json
import random
import tkinter as tk
from tkinter import messagebox

with open('words.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

num_entries = len(data)

# Create a function to check the user's answer.
def check_answer(user_choice):
    global question_count, score, wrong_answers
    correct_answer = options.index(random_entry)
    if user_choice == correct_answer:
        score += 1
        result_label.config(text=f"正確答案！ {chinese_translation} {word} ({part_of_speech}.) 目前分數:{score}", fg='green')
    else:
        result_label.config(text=f"答案錯誤，正確答案是選項 {correct_answer}: {chinese_translation} {word} ({part_of_speech}.) 目前分數:{score}", fg='red')
        wrong_answers.append((chinese_translation, word, part_of_speech))
    question_count += 1
    if question_count < total_questions:
        next_question()
    else:
        show_final_score()

def next_question():
    global random_entry, word, definitions, chinese_translation, part_of_speech, options
    random_entry = random.choice(data)
    word = random_entry["word"]
    definitions = random_entry["definitions"]
    chinese_translation = definitions[0]["text"]
    part_of_speech = definitions[0]["partOfSpeech"]
    options = [random.choice(data) for _ in range(3)]
    options.append(random_entry)
    random.shuffle(options)

    if quiz_type == "1":
        question_label.config(text=f"英文：{word} ({part_of_speech}.) ({question_count + 1}/{total_questions})")
    else:
        question_label.config(text=f"中文：{chinese_translation} ({part_of_speech}.) ({question_count + 1}/{total_questions})")

    for i, option in enumerate(options, start=1):
        if quiz_type == "1":
            option_buttons[i - 1].config(text=f"{i}. {option['definitions'][0]['text']}")
        else:
            option_buttons[i - 1].config(text=f"{i}. {option['word']}")
    result_label.config(text="", fg='black')

def show_final_score():
    global wrong_answers
    percent_score = score * (100 / total_questions)
    result_label.config(text=f"試題結束! 作答成績: {round(float(percent_score))}%", fg='black')

    if len(wrong_answers) > 0:
        wrong_answers_str = "\n".join([f"{answer[0]} {answer[1]} ({answer[2]}.)" for answer in wrong_answers])
        wrong_answers_label.config(text="錯誤答案列表:\n" + wrong_answers_str)
    else:
        wrong_answers_label.config(text="恭喜！沒有錯誤答案。")
    wrong_answers_label.pack()

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
definitions = []
chinese_translation = ""
part_of_speech = ""
options = []

def start_quiz():
    global quiz_type, total_questions, question_count, score, wrong_answers
    quiz_type = quiz_type_var.get()
    total_questions = int(total_questions_entry.get())
    question_count = 0
    score = 0
    wrong_answers = []
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
