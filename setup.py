import os
from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8") as f:
        return f.read()


setup(
    name="WowSkin",  # 项目名称
    version="1.0.0",  # 初始版本号
    author="WowRobo",
    author_email="leo.xiao@wowrobo.com",
    description="Python library for interfacing with a WowSkin intelligent magnetic sensing circuit, based on AnySkin and ReSkin.",
    long_description=read("README.md"),  # 使用 README.md 作为详细描述
    long_description_content_type="text/markdown",  # 确保 README 是 Markdown 格式
    packages=find_packages(),
    include_package_data=True,  # 包括额外的文件
    package_data={
        "wow_skin.visualizations": ["images/wowskin_bg.png"],  # 如果需要额外文件
    },
    install_requires=[
        "numpy>=1.21.3",
        "pyserial>=3.5",
        "pygame>=2.6.0"
    ],  # 项目依赖
    python_requires=">=3.8",  # 最低 Python 版本要求
    url="https://github.com/WowRobo-Robotics/WowSkin.git",
    entry_points={
        "console_scripts": [
            "wowskin_viz=wowskin_viz:default_viz"  # 根目录中的命令行入口点
        ],
    },
    license="MIT",  # 原项目的 MIT 许可证
)
