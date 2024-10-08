import yaml
import dashscope
from http import HTTPStatus
import json
import sys


yaml_file_path = "./info.yaml"
with open(yaml_file_path, 'r', encoding='utf-8') as file:
    yaml_str = yaml.safe_load(file)

ali_api_key = yaml_str["ali_api_key"]

# 设置环境变量
dashscope.api_key = ali_api_key


def agent_update(assistant_id, instructions, midel="qwen-max"):
    # 更新智能体
    assistants = dashscope.Assistants.update(
        assistant_id=assistant_id,
        model=midel,
        instructions=instructions
    )
    return assistants


def agent_list(limit):
    # 列出已存在的agents
    assistants = dashscope.Assistants.list(limit=limit,
                                           order='desc',
                                           after='',
                                           before='')

    return assistants


def agent_retrieve(assistant_id):
    # 查找智能体
    assistant = dashscope.Assistants.retrieve(assistant_id)
    return assistant


def chat_create():
    # 创建一个窗口
    thread = dashscope.Threads.create()
    return thread


def chat_del(thread_id):
    # 删除一个窗口
    dashscope.Threads.delete(thread_id)


def chat_recreate(thread_id):
    # 重新创建一个窗口
    chat_del(thread_id)
    thread = chat_create()
    return thread


def verify_status_code(res):
    if res.status_code != HTTPStatus.OK:
        # print('Failed: ')
        # print(res)
        sys.exit(res.status_code)


def msg_retrieve(msg_id, thread_id):
    message = dashscope.Messages.retrieve(message_id=msg_id, thread_id=thread_id)  # 查看消息
    return message


def send_msg(user_msg, thread_id, assistant_id):
    dashscope.Messages.create(thread_id, content=user_msg)
    stream_run = dashscope.Runs.create(thread_id=thread_id, assistant_id=assistant_id, stream=True)

    tokens = 0
    for event, msg in stream_run:
        print(event)
        print(msg)
        if event == "thread.message.delta":
            text = msg['delta']['content']['text']['value']
            yield text
        if event == "thread.run.completed":
            token = msg['usage']["total_tokens"]
            yield token


def agent_dialog_develop(messages):
    assistant_id = messages["assistant_id"]
    thread_id = messages["chat_id"]
    user_msg = messages["user_msg"]
    instructions = messages["instructions"]

    assistant_old = dashscope.Assistants.retrieve(assistant_id)
    assistants_new = agent_update(assistant_id, instructions, "qwen-max")
    res, tokens = send_msg(user_msg, thread_id, assistant_id)

    yield res, tokens, assistant_id, thread_id


def agent_dialog(messages):
    assistant_id = messages["assistant_id"]
    thread_id = messages["chat_id"]
    user_msg = messages["user_msg"]

    res = send_msg(user_msg, thread_id, assistant_id)

    yield res, assistant_id, thread_id











