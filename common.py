import datetime
import random
import re


def extract_numbers(input_string):
    pattern = r"\d+"
    matches = re.findall(pattern, input_string)
    return matches[0]


def get_current_time():
    current_time = datetime.datetime.now()
    time_string = current_time.strftime("%Y-%m-%d-%H-%M-%S")
    return time_string


def random_wiat_number():
    mu = 10  # 均值
    sigma = 2  # 标准差，可以根据需要进行调整

    # 生成正态分布的随机数
    random_num = random.gauss(mu, sigma)

    # 如果生成的随机数小于0，则将其设置为0
    random_num = max(random_num, 0)

    return random_num