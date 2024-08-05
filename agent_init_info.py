from http import HTTPStatus
import dashscope
from PIL import Image
import requests
from io import BytesIO
import yaml


yaml_file_path = "./info.yaml"
with open(yaml_file_path, 'r', encoding='utf-8') as file:
    yaml_str = yaml.safe_load(file)

ali_api_key = yaml_str["ali_api_key"]

# 设置环境变量
dashscope.api_key = ali_api_key




def ask_question(messages, model_name="qwen-max"):
    responses = dashscope.Generation.call(model_name,
                                          messages=messages,
                                          result_format='message',  # set the result to be "message"  format.
                                          stream=True,  # set streaming output
                                          incremental_output=True  # get streaming output incrementally
                                          )
    return responses


def generate_instructions(init_mgs, model_name="qwen-max"):
    init_messages = init_mgs["info"]
    info_str = yaml_str["info"]
    content_instructions = info_str["content_instructions"] + f"{init_messages}"
    mes = [
        {"role": "system", "content": 'You are a helpful assistant.'},
        {"role": "user", "content": content_instructions}
    ]
    reply = ask_question(mes, model_name)
    out = ""
    for res in reply:
        if res.status_code == HTTPStatus.OK:
            out = out + res.output.choices[0]['message']['content']
    return {"instructions" : out}





def generate_info(init_mgs, model_name="qwen-max"):
    name = init_mgs["name"]
    init_messages = init_mgs["info"]
    info_str = yaml_str["info"]
    content_description = info_str["content_description"] + f"{init_messages}"
    content_instructions = info_str["content_instructions"] + f"{init_messages}"
    content_opening = info_str["content_opening"] + f"{init_messages}"
    content_asking = info_str["content_asking"] + f"{init_messages}"

    content_list = [content_description, content_instructions, content_opening]
    name_list = ["description", "instructions", "opening", "asking"]

    messages_list = []
    for i in content_list:
        messages_ = [
            {"role": "system", "content": 'You are a helpful assistant.'},
            {"role": "user", "content": i}
        ]
        messages_list.append(messages_)
    messages05 = [{"role": "user", "content": content_asking}]
    messages_list.append(messages05)

    no_answered_list = []
    # 调用ask_question方法提问
    for mes in messages_list:
        res = ask_question(mes, model_name)
        no_answered_list.append(res)

    # 查询答案
    reply_all_dic = {}
    for i, reply in zip(name_list, no_answered_list):
        out = ""
        for res in reply:
            if res.status_code == HTTPStatus.OK:
                out = out + res.output.choices[0]['message']['content']
        reply_all_dic[i] = out
    reply_all_dic["name"] = name
    return reply_all_dic


def draw_image(init_messages):
    img_info = yaml_str["img_info"]
    img_disc = img_info["img_disc"] + f"{init_messages}"
    # 生成图片
    task = dashscope.ImageSynthesis.async_call(model=dashscope.ImageSynthesis.Models.wanx_v1,
                                               prompt=img_disc,
                                               n=1,
                                               size='1024*1024')
    status = dashscope.ImageSynthesis.fetch(task)
    task_status = status.output.task_status
    rsp = dashscope.ImageSynthesis.wait(task)

    img_url = rsp.output.results[0].url
    get_img = requests.get(img_url)
    image_data = get_img.content.hex()
    image = Image.open(BytesIO(bytes.fromhex(image_data)))

    resized_image = image.resize((128, 128))
    binary_image_data = resized_image.tobytes().hex()

    return binary_image_data


def init_agent(init_messages):
    init_info = generate_info(init_messages)

    # 创建智能体
    name = "智能体01"
    description = init_info["description"]
    instructions = yaml_str["system_prompt_template"]["sys03"]

    assistant = dashscope.Assistants.create(
        model='qwen-max',
        name=name,
        description=description,
        instructions=instructions)  # instructions

    chat = dashscope.Threads.create()
    return init_info, assistant, chat




