from openai import OpenAI
import json

with open("api_key.txt", "r") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)

with open("dialog.json", "r") as f:
    dialog = json.load(f)


first_response = "是。"
question_classification = "。以上問題是是非題嗎"
question_filter = "如果該問題的答案在問答中找不到，請回答不知道\
                請先思考以上問題是否為是非題。如果該問題不是是非題，請回答 不知道，並且不做任何補充說明\
                。如果問題是是非題，請用是、不是、不知道來回答。"

system_message = "你是一個有幫助的機器人。你只會回答：是、不是、不知道其中一個."
system_message = "你是一個有幫助的機器人"


def get_response(question, answer):
    prompt = f"以上是關於資工系教授的問答。接下來，請你當一個是非題回答機器人，根據檔案回答關於{answer}的是非題。\
        你只能回答是、不是、和不知道。請不要回答是、不是、不知道以外的東西\
        請不要做任何補充說明，回答是、不是、不知道就好。\
        如果以上的問答沒有這題的答案，請回答不知道，不要亂回答\
        當我們問的問題不是是非題時，請回答不知道。例如：他的專業是什麼？ 請回答：不知道\
        當我們猜：是{answer}嗎？或類似的問題，可以回答是."

    messages = (
        [{"role": "system", "content": system_message}]
        + dialog
        + [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": first_response},
        ]
    )

    messages.append({"role": "user", "content": question + question_filter})
    # print(messages)
    response = client.chat.completions.create(
        model="gpt-4-1106-preview", messages=messages, temperature=0
    )
    print(response)
    return response.choices[0].message.content


if __name__ == "__main__":
    while 1:
        question = input("user:")
        response = get_response(question)
        print("gpt:", response)
