import json

# 读取现有的 vocab.json 文件内容
try:
    with open('vocab.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    # 如果文件不存在，创建一个空的数据列表
    data = []

def add_new_word():
    # 输入新单词的信息
    word = input("请输入新单词：")
    
    # 检查单词是否已存在
    for entry in data:
        if entry["word"] == word:
            print(f"单词 '{word}' 已经存在于词汇表中。")
            return  # 如果单词已存在，不进行后续操作
    
    chinese_translation = input("请输入中文翻译：")
    part_of_speech = input("请输入词性：")

    # 创建新单词的字典
    new_word = {
        "word": word,
        "chinese": chinese_translation,
        "partOfSpeech": part_of_speech
    }

    # 将新单词添加到数据列表中
    data.append(new_word)

    # 保存更新后的数据到 vocab.json 文件
    with open('vocab.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"已成功添加新单词：{word}")

# 主程序
while True:
    print("1. 添加新单词")
    print("2. 退出程序")
    choice = input("请选择操作：")

    if choice == "1":
        add_new_word()
    elif choice == "2":
        break
    else:
        print("无效的选择，请重新选择。")

print("程序已退出。")
