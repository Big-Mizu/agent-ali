from flask import Flask, request, jsonify
import json
from agent_init_info import generate_instructions, draw_image, init_agent
import dashscope
from agent_utils import agent_dialog, agent_dialog_develop, chat_recreate


flask_app = Flask(__name__)


@flask_app.route('/init_ag', methods=['post'])
def init_ag():
    """
    {"info" : "你是一个 Python 技术专家，熟练掌握 Python 技术栈相关知识，具有丰富的 Python 实战经验，参与过众多行业的应用设计和研发工作。你非常擅长 Python 教学和指导，能帮助技术和系统设计人员快速掌握相关技能，以及解决其遇到的问题。",
    "name" : "智能体02"}
    """
    data = request.get_data().decode('utf-8')
    init_messages = json.loads(data)
    init_info, assistant, chat = init_agent(init_messages)
    out = {
        "init_info": init_info,
        "assistant_id": assistant.id,
        "chat_id": chat.id
    }
    return jsonify(out)


@flask_app.route('/draw_img', methods=['post'])
def draw_img():
    """
    {"info" : "作为一个天气预报员，可以通过用户提供的城市，查询当天的天气情况，并提示用户可以穿着的衣服搭配，同时给出用户正能量的鼓励和加油。"}
    {"info" : "你是一个 Python 技术专家，熟练掌握 Python 技术栈相关知识，具有丰富的 Python 实战经验，参与过众多行业的应用设计和研发工作。你非常擅长 Python 教学和指导，能帮助技术和系统设计人员快速掌握相关技能，以及解决其遇到的问题。"}
    """
    data = request.get_data().decode('utf-8')
    init_messages = json.loads(data)
    img = draw_image(init_messages["info"])
    out = {'img': img}
    return jsonify(out)


@flask_app.route('/generate_instructions', methods=['post'])
def gen_instructions():
    """
    {"info" : "你是一个 Python 技术专家，熟练掌握 Python 技术栈相关知识，具有丰富的 Python 实战经验，参与过众多行业的应用设计和研发工作。你非常擅长 Python 教学和指导，能帮助技术和系统设计人员快速掌握相关技能，以及解决其遇到的问题。"}
    """
    data = request.get_data().decode('utf-8')
    init_messages = json.loads(data)
    out = generate_instructions(init_messages)

    return jsonify(out)


@flask_app.route('/ag_dialog_develop', methods=['post'])
def ag_dialog_develop():
    """
    对话接口 - 未发布
    {
    "assistant_id": "asst_66ed9b35-e450-4aa8-9996-50480d76d045",
    "chat_id" : "thread_069fdf61-18a9-49fe-86e9-8524d247a542",
    "user_msg" : "列举10位中国近代史的名人",
    "instructions": " # 角色 你是一个 Python 技术专家，熟练掌握 Python 技术栈相关知识，具有丰富的 Python 实战经验，参与过众多行业的应用设计和研发工作。你非常擅长 Python 教学和指导，能帮助技术和系统设计人员快速掌握相关技能，以及解决其遇到的问题。 ## 技能 ### 技能 1：Python 教学 1. 你可以为技术和系统设计人员提供 Python 技术栈相关的教学服务，包括基础知识、进阶技能、实战经验等方面的内容。 2. 根据学员的需求和水平，制定个性化的教学计划和课程内容，帮助学员快速掌握相关技能。 3. 通过在线课程、面对面教学、实践项目等方式，为学员提供全方位的教学支持和指导。 ### 技能 2：Python 指导 1. 你可以为技术和系统设计人员提供 Python 相关的技术指导和支持，帮助他们解决在工作中遇到的问题。 2. 根据问题的具体情况，提供针对性的解决方案和建议，帮助他们提高工作效率和质量。 3. 通过在线交流、电话咨询、现场指导等方式，为学员提供及时的技术支持和服务。 ### 技能 3：Python 项目经验分享 1. 你可以分享自己在 Python 项目开发中的实战经验和心得体会，帮助技术和系统设计人员更好地理解和应用 Python 技术。 2. 通过案例分析、代码演示、项目实战等方式，为学员提供更加深入和全面的学习体验。 3. 与学员进行互动交流，分享自己的经验和见解，帮助他们提高技术水平和实践能力。 ## 限制 - 只讨论与 Python 技术相关的内容，拒绝回答与 Python 技术无关的话题。 - 所输出的内容必须按照给定的格式进行组织，不能偏离框架要求。 - 总结部分不能超过 100 字。 - 请使用 Markdown 的 ^^ 形式说明引用来源。 "
    }
    """
    data = request.get_data().decode('utf-8')
    useful_messages = json.loads(data)
    res, assistant_id, chat_id = agent_dialog_develop(useful_messages)
    out = {
        "res": res,
        "assistant_id": assistant_id,
        "chat_id": chat_id
    }
    return jsonify(out)


@flask_app.route('/ag_dialog', methods=['post'])
def ag_dialog():
    """
    对话接口
    {
    "assistant_id": "asst_404ad7ad-1880-4b9d-bc79-186fd104a09e",
    "chat_id" : "thread_2dd03bdf-f680-4f7e-8130-73cb31ffbef1",
    "user_msg" : "列举10位中国近代史的名人"
    }
    """
    data = request.get_data().decode('utf-8')
    useful_messages = json.loads(data)
    res, assistant_id, chat_id = agent_dialog(useful_messages)
    out = {
        "res": res,
        "assistant_id": assistant_id,
        "chat_id": chat_id
    }
    return jsonify(out)


@flask_app.route('/chat_recreate', methods=['post'])
def chat_re():
    """
    重置窗口
    {"chat_id" : "thread_7f35caad-6ef0-4d0a-9029-b485d963f170"}
    """
    data = request.get_data().decode('utf-8')
    data_ = json.loads(data)
    thread = chat_recreate(data_["chat_id"])
    out = {'chat_id': thread.id}
    return jsonify(out)


@flask_app.route('/del_ag', methods=['post'])
def del_ag():
    """
    {"assistant_id": "asst_d337e1b4-3f15-49fe-b4ca-e120f3c9b389"}
    """
    data = request.get_data().decode('utf-8')
    assistant_id = json.loads(data)

    try:
        dashscope.Assistants.delete(assistant_id["assistant_id"])
        out = {"code": 0}
    except:
        out = {"code": 1}

    return jsonify(out)


if __name__ == '__main__':
    flask_app.run(debug=True, host="0.0.0.0", port="5000", use_reloader=False)
    print()
