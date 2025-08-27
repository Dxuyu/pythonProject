import time
from datetime import datetime

# 吉凶列表及其解释
sz = ["大安", "留连", "速喜", "赤口", "小吉", "空亡"]
sz1 = [
    "诸事皆宜，谋事顺利，求财可得，行人归来，疾病痊愈",
    "象征迟滞、反复与拖延，诸事不顺，容易发生纠纷或争执，求财不易，行人未归，疾病缠身",
    "快速、积极与喜庆，诸事顺利，喜事临门，进展快速，求财可得，行人将至，疾病好转",
    "主口舌、争执、是非，容易发生争吵、纠纷，或有官非、伤灾等情况，求财不利，行人有惊慌",
    "吉利、顺利、小有成就，有和合、喜庆之意，求财可得，行人将至，疾病转好",
    "主虚无、空洞、无力，代表事情没有结果，或信息不明确，谋事难成，求财无获，行人未归，疾病凶险"
]


# 返回当前时辰对应的数字（1-12）
def sj():
    localtime = time.localtime(time.time())
    s = localtime.tm_hour

    if s >= 23 or s < 1:
        return 1
    elif s >= 1 and s < 3:
        return 2
    elif s >= 3 and s < 5:
        return 3
    elif s >= 5 and s < 7:
        return 4
    elif s >= 7 and s < 9:
        return 5
    elif s >= 9 and s < 11:
        return 6
    elif s >= 11 and s < 13:
        return 7
    elif s >= 13 and s < 15:
        return 8
    elif s >= 15 and s < 17:
        return 9
    elif s >= 17 and s < 19:
        return 10
    elif s >= 19 and s < 21:
        return 11
    elif s >= 21 and s < 23:
        return 12


# 获取当前日期
def get_current_date():
    now = datetime.now()
    return now.year, now.month, now.day


# 获取农历信息
current_year, current_month, current_day = get_current_date()
lunar_info = None

try:
    from lunar_python import Solar


    class LunarTool:
        @classmethod
        def convert(cls, year, month, day):
            try:
                solar = Solar(year, month, day, 0, 0, 0)
                lunar = solar.getLunar()
                return {
                    '月': lunar.getMonth(),
                    '日': lunar.getDay(),
                    '月中文': lunar.getMonthInChinese(),
                    '日中文': lunar.getDayInChinese()
                }
            except Exception as e:
                print(f"农历转换错误: {e}")
                return None


    lunar_info = LunarTool.convert(current_year, current_month, current_day)
    if lunar_info:
        print(f"\n当前农历：{lunar_info['月中文']}{lunar_info['日中文']}")
except ImportError:
    print("\n未安装lunar-python库，无法进行农历转换")
except Exception as e:
    print(f"\n发生错误: {e}")


# 计算吉凶结果
def jg():
    if not lunar_info:
        print("无法获取农历信息，无法计算")
        return

    y1 = abs(lunar_info['月'])
    r1 = lunar_info['日']
    s1 = sj()

    def calculate_positions(numbers):
        current_pos = 1  # 起始位置
        results = []

        for num in numbers:
            # 计算最终位置
            final_pos = (current_pos + num - 1) % 6
            if final_pos == 0:
                final_pos = 6

            # 获取对应的吉凶和解释（注意索引从0开始）
            sz_index = final_pos - 1
            results.append({
                '数字': num,
                '位置': final_pos,
                '吉凶': sz[sz_index],
                '解释': sz1[sz_index]
            })

            current_pos = final_pos

        return results

    input_numbers = [y1, r1, s1]
    results = calculate_positions(input_numbers)

    print("\n计算结果：")
    for i, result in enumerate(results, 1):
        print(f"{result['吉凶']} - {result['解释']}")

    return results


# 保持按需计算：仅在接口调用时执行 jg()
# 后端接口
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)


# 1. 提供HTML页面（前端入口）
@app.route('/')
def index():
    # 直接返回同目录下的 index.html
    return send_file('index.html')


# 2. 处理前端POST请求（接收数据并返回结果）
@app.route('/api/suangua', methods=['POST'])
def api_suangua():
    try:
        results = jg()
        if not results:
            return jsonify({'status': 'error', 'message': '无法计算，请检查农历依赖或时间获取'}), 500

        # 将三步结果拼为多行文字
        lines = [f"{item['吉凶']} - {item['解释']}" for item in results]
        text = "\n".join(lines)
        return jsonify({'status': 'success', 'message': text})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    # 启动服务器，允许外部访问（debug=True开发模式）
    app.run(host='0.0.0.0', port=5000, debug=True)

