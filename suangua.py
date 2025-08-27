import time

sz=["大安","留连","速喜","赤口","小吉","空亡"]
sz1=["诸事皆宜，谋事顺利，求财可得，行人归来，疾病痊愈","象征迟滞、反复与拖延，诸事不顺，容易发生纠纷或争执，求财不易，行人未归，疾病缠身","快速、积极与喜庆，诸事顺利，喜事临门，进展快速，求财可得，行人将至，疾病好转","主口舌、争执、是非，容易发生争吵、纠纷，或有官非、伤灾等情况，求财不利，行人有惊慌","吉利、顺利、小有成就，有和合、喜庆之意，求财可得，行人将至，疾病转好","主虚无、空洞、无力，代表事情没有结果，或信息不明确，谋事难成，求财无获，行人未归，疾病凶险"]

#返回时分
def sj():
    localtime = time.localtime(time.time())
    s=localtime.tm_hour
    f=localtime.tm_min
    if s>=23 or s<1:
        return 1
    elif s>=1 and s<3:
        return 2
    elif s>=3 and s<5:
        return 3
    elif s>=5 and s<7:
        return 4
    elif s>=7 and s<9:
        return 5
    elif s>=9 and s<11:
        return 6
    elif s>=11 and s<13:
        return 7
    elif s>=13 and s<15:
        return 8
    elif s>=15 and s<17:
        return 9
    elif s>=17 and s<19:
        return 10
    elif s>=19 and s<21:
        return 11
    elif s>=21 and s<23:
        return 12
# print(sj())


from datetime import datetime


def get_current_date():
    """获取当前日期并返回年、月、日"""
    # 获取当前日期时间
    now = datetime.now()
    # 提取年、月、日
    year = now.year
    month = now.month
    day = now.day

    return year, month, day

# 调用函数获取当前日期
current_year, current_month, current_day = get_current_date()
# 结合之前的农历转换功能（如果需要）
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

    # 转换当前日期为农历
    lunar_info = LunarTool.convert(current_year, current_month, current_day)
    # if lunar_info:
    #     print(f"\n当前农历：{lunar_info['月中文']}{lunar_info['日中文']}")
    #     print(f"农历月：{abs(lunar_info['月'])}")
    #     print(f"农历日：{lunar_info['日']}")
except ImportError:
    print("\n未安装lunar-python库，无法进行农历转换")
except Exception as e:
    print(f"\n发生错误: {e}")


def jg():
    y1 = abs(lunar_info['月'])
    r1 = lunar_info['日']
    s1=sj()
    # print(y1,r1,s1)
    def calculate_positions(numbers):
        # 调整索引从1开始
        indexed_sz = [None] + sz  # 现在indexed_sz[1]到indexed_sz[6]对应六个元素

        current_pos = 1  # 起始位置
        results = []

        for num in numbers:
            # 计算最终位置
            final_pos = (current_pos + num - 1) % 6
            # 处理取模为0的情况（对应位置6）
            if final_pos == 0:
                final_pos = 6

            # 记录结果
            results.append({
                '数字': num,
                '位置': final_pos,
                '对应元素': indexed_sz[final_pos]
            })

            # 更新当前位置为本次的最终位置
            current_pos = final_pos

        return results

    # 使用示例
    if __name__ == "__main__":
        # 可以替换为任意数字序列
        input_numbers = [y1, r1, s1]

        # 计算结果
        results = calculate_positions(input_numbers)

        # 打印结果
        print("计算结果：")
        for result in results:
            print(f"{result['对应元素']}")
    return
a=jg()