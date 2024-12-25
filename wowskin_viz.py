#!/usr/bin/env python
#这段代码是基于AnySkin的代码改写和优化

import time
import numpy as np
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import sys
import pygame
from datetime import datetime
#from anyskin import AnySkinProcess
from sensor_proc import AnySkinProcess
import argparse


def visualize(port, file=None, viz_mode="3axis", scaling=7.0, record=False):

    # 如果没有指定 file，则从实时串口读取数据
    if file is None:
        sensor_stream = AnySkinProcess(num_mags=5, port=port)
        sensor_stream.start()
        time.sleep(1.0)  # 等待串口连接稳定
        filename = "data/data_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    else:
        # 加载本地文件的数据
        load_data = np.loadtxt(file)

    # 初始化 pygame
    pygame.init()
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # 读取背景图
    bg_image_path = os.path.join(dir_path, "images/wowskin_bg.png")
    bg_image = pygame.image.load(bg_image_path)
    image_width, image_height = bg_image.get_size()

    # 设定窗口的大小，让宽度固定为 400，高度依照图片比例缩放
    aspect_ratio = image_height / image_width
    desired_width = 400
    desired_height = int(desired_width * aspect_ratio)

    # 各个芯片在图片上的坐标
    chip_locations = np.array(
        [
            [201, 238],  # center
            [126, 238],  # left
            [275, 238],  # right
            [201, 163],  # up
            [201, 312],  # down
        ]
    )
    # 每个芯片在 XY 平面对应的旋转角度
    chip_xy_rotations = np.array([-np.pi / 2, -np.pi / 2, np.pi, np.pi / 2, 0.0])

    # 把背景图缩放到上面设定的大小
    bg_image = pygame.transform.scale(bg_image, (desired_width, desired_height))

    # 创建 pygame 窗口
    window = pygame.display.set_mode((desired_width, desired_height), pygame.SRCALPHA)
    pygame.display.set_caption("WowSkin Sensor Data Visualization")

    # 准备一个背景层，这里填充一个颜色再贴上背景图
    background_surface = pygame.Surface(window.get_size(), pygame.SRCALPHA)
    background_color = (234, 237, 232, 255)
    background_surface.fill(background_color)
    background_surface.blit(bg_image, (0, 0))

    # ========== 按钮相关设置 ==========
    # 定义按钮矩形(位置和大小)
    button_rect = pygame.Rect(10, 10, 90, 40)
    # 准备字体
    button_font = pygame.font.SysFont(None, 24)
    # 按钮上显示的文字
    button_text_surface = button_font.render("Reset", True, (255, 255, 255))

    def visualize_data(data):
        """
        将传感器数据在界面上可视化（磁场向量或磁场强度）
        """
        data = data.reshape(-1, 3)  # 5*3 => [ [x1,y1,z1], ..., [x5,y5,z5] ]
        data_mag = np.linalg.norm(data, axis=1)  # 求每个三轴向量的模

        # 绘制每个芯片的数据
        for magid, chip_location in enumerate(chip_locations):
            if viz_mode == "magnitude":
                # 以圆形面积代表磁场强度
                pygame.draw.circle(
                    window, (255, 83, 72), chip_location, data_mag[magid] / scaling
                )
            elif viz_mode == "3axis":
                # z 轴的正负分别用实心圆和空心圆
                if data[magid, -1] < 0:
                    width = 2  # 空心圆
                else:
                    width = 0  # 实心圆

                pygame.draw.circle(
                    window,
                    (255, 0, 0),  # 用红色圆表示 z 轴的大小
                    chip_location,
                    abs(data[magid, -1]) / scaling,
                    width,
                )

                # 画 xy 平面的箭头 (绿色)
                arrow_start = chip_location
                rotation_mat = np.array(
                    [
                        [
                            np.cos(chip_xy_rotations[magid]),
                            -np.sin(chip_xy_rotations[magid]),
                        ],
                        [
                            np.sin(chip_xy_rotations[magid]),
                            np.cos(chip_xy_rotations[magid]),
                        ],
                    ]
                )
                data_xy = np.dot(rotation_mat, data[magid, :2])
                arrow_end = (
                    chip_location[0] + data_xy[0] / scaling,
                    chip_location[1] + data_xy[1] / scaling,
                )
                pygame.draw.line(window, (0, 255, 0), arrow_start, arrow_end, 2)

    def get_baseline():
        """
        从实时数据流中采集一定数量的样本，取平均作为新的 baseline
        """
        baseline_data = sensor_stream.get_data(num_samples=5)
        baseline_data = np.array(baseline_data)[:, 1:]  # 跳过时间戳列
        baseline = np.mean(baseline_data, axis=0)
        return baseline

    # 如果没有传入文件，就要先获取一个 baseline
    if file is None:
        time.sleep(0.1)
        baseline = get_baseline()
    else:
        # 如果是加载文件，就无需 baseline（或在下面随时设）
        baseline = None

    frame_num = 0
    running = True
    data = []      # 记录采样到的数据
    data_len = 30000  # 如果用加载文件的方式，这里控制索引
    clock = pygame.time.Clock()
    FPS = 60

    print("Pygame窗口已创建，请点击该窗口使其获取焦点。若需按键或按钮重置 baseline，请点击/按键。")

    # 主循环
    while running:
        # 先把背景贴上
        window.blit(background_surface, (0, 0))

        # ========== 绘制按钮 ==========
        pygame.draw.rect(window, (70, 130, 180), button_rect)  # 蓝色矩形按钮
        text_x = button_rect.x + (button_rect.width - button_text_surface.get_width()) / 2
        text_y = button_rect.y + (button_rect.height - button_text_surface.get_height()) / 2
        window.blit(button_text_surface, (text_x, text_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 鼠标点击检测
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(f"Mouse clicked at ({x}, {y})")
                # 判断是否点击在按钮区域
                if button_rect.collidepoint(x, y):
                    print("Button clicked! Reset baseline...")
                    if file is None:
                        baseline = get_baseline()
                    else:
                        # 如果用文件播放，则自行决定怎么处理 baseline
                        baseline = np.zeros(15)  # 或根据实际需求重置

            # 键盘按下检测（保留 b 键功能）
            if event.type == pygame.KEYDOWN:
                print("Key pressed:", event.key, event.unicode)
                if event.key == pygame.K_b:
                    print("Reset baseline data via key b!")
                    if file is None:
                        baseline = get_baseline()
                    else:
                        baseline = np.zeros(15)  # 或按需处理

        # 获取传感器数据（实时或从文件）
        if file is not None:
            # 假设一次只取一行数据
            sensor_data = load_data[data_len]
            data_len += 24  # 这里原作者逻辑是每帧跳 24 行，你可自行调整
            # 若 baseline 未初始化，就初始化为 0
            if baseline is None:
                baseline = np.zeros_like(sensor_data)
            # 这里可以决定是否减 baseline
            data_to_show = sensor_data - baseline
        else:
            # 实时读取 1 条数据
            sensor_data = sensor_stream.get_data(num_samples=1)[0][1:]
            data_to_show = sensor_data - baseline
            data.append(data_to_show)  # 若需要记录

        # 可视化当前数据
        visualize_data(data_to_show)
        frame_num += 1

        # 更新 Pygame 窗口
        pygame.display.update()
        clock.tick(FPS)

    # 程序结束，清理资源
    pygame.quit()

    # 如果是实时采集，停止线程
    if file is None:
        sensor_stream.pause_streaming()
        sensor_stream.join()
        data = np.array(data)
        if record:
            np.savetxt(f"{filename}.txt", data)


def default_viz(argv=sys.argv):
    visualize(port=argv[1])


if __name__ == "__main__":
    # fmt: off
    parser = argparse.ArgumentParser(description="AnySkin streaming visualization with baseline reset button.")
    parser.add_argument("-p", "--port", type=str, help="port to which the microcontroller is connected", default="/dev/cu.usbmodem101")
    parser.add_argument("-f", "--file", type=str, help="path to load data from", default=None)
    parser.add_argument("-v", "--viz_mode", type=str, help="visualization mode", default="3axis", choices=["magnitude", "3axis"])
    parser.add_argument("-s", "--scaling", type=float, help="scaling factor for visualization", default=7.0)
    parser.add_argument('-r', '--record', action='store_true', help='record data')
    args = parser.parse_args()
    # fmt: on
    visualize(args.port, args.file, args.viz_mode, args.scaling, args.record)
