import random

WORDSET_1 = [
    "행복한", "사랑스러운", "즐거운", 
    "밥먹는",
]

WORDSET_2 = [
    "노란", "초록", "하늘색", 
    "핑크색", "파란", "빨간"
]

WORDSET_3 = [
    "강아지", "코끼리", "펭귄", "꽃사슴", 
    "해바라기", "튤립"
]

def generate_username():
    first_word = WORDSET_1[random.randint(0, len(WORDSET_1)-1)]
    second_word = WORDSET_2[random.randint(1, len(WORDSET_2)-1)]
    third_word = WORDSET_3[random.randint(1, len(WORDSET_3)-1)]
    username = first_word + second_word + third_word
    return username


print("ahahah")
print(generate_username())