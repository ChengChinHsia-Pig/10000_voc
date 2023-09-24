import json
import random
import os

with open('words.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

num_entries = len(data)

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')

print(f"""
國高中單字詞彙測驗系統
國中2000單+高中7000單混合題庫
共有 {num_entries} 個單字
By ChengChinHsia 2023, All Right Reserved.
""")
print("選擇測驗類型：")
print("1. 英文到中文")
print("2. 中文到英文")
quiz_type = input("請輸入選擇的測驗類型編號： ")

if quiz_type == "1":
    print("您選擇了英文到中文測驗。")
elif quiz_type == "2":
    print("您選擇了中文到英文測驗。")
else:
    print("無效的選擇，請選擇 1 或 2 來選擇測驗類型。")
    exit()

total_questions = int(input("請輸入總題數： "))

question_count = 0
score = 0

wrong_answers = []

while question_count < total_questions:
    clear_terminal()
    random_entry = random.choice(data)
    word = random_entry["word"]
    definitions = random_entry["definitions"]
    chinese_translation = definitions[0]["text"]
    part_of_speech = definitions[0]["partOfSpeech"]
    options = [random.choice(data) for _ in range(3)]
    options.append(random_entry)
    random.shuffle(options)
    if quiz_type == "1":
        print(f"英文：{word} ({part_of_speech}.) ({question_count+ 1}/{total_questions})")
        print("請選擇正確的中文翻譯：")
    else:
        print(f"中文：{chinese_translation} ({part_of_speech}.) ({question_count + 1}/{total_questions})")
        print("請選擇正確的英文單字：")
    for i, option in enumerate(options, start=1):
        if quiz_type == "1":
            print(f"{i}. {option['definitions'][0]['text']}")
        else:
            print(f"{i}. {option['word']}")
    user_answer = input("請輸入您的答案的編號： ")
    correct_answer = options.index(random_entry) + 1
    if int(user_answer) == correct_answer:
        score += 1
        print(f"正確答案！ {chinese_translation} {word} ({part_of_speech}.) 目前分數:{score}")
    else:
        print(f"答案錯誤，正確答案是選項 {correct_answer}: {chinese_translation} {word} ({part_of_speech}.) 目前分數:{score}")
        wrong_answers.append((chinese_translation, word, part_of_speech))
    question_count += 1
clear_terminal()
percent_score = score * (100 / total_questions)
print(f"試題結束! 作答成績: {round(float(percent_score))}%")

if len(wrong_answers) > 0:
    print("錯誤答案列表：")
    for answer in wrong_answers:
        print(f"{answer[0]} {answer[1]} ({answer[2]}.)")