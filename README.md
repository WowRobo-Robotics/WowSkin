# WowSkin

WowSkin 是一款针对智能触觉皮肤设计的开源解决方案。本项目基于 [AnySkin](https://any-skin.github.io/) 和 [ReSkin](https://reskin.dev/) 的开源基础，加入了针对特定应用场景的改进和新功能。

## 功能特点

- **增强的磁传感器驱动**：提升了与 MLX90393 等传感器的兼容性和性能。
- **实时可视化**：通过自定义可视化工具，轻松查看磁场数据。
- **改进的算法**：提供更精确的 XYZ 磁场分析，并降低噪声。
- **灵活的架构**：模块化代码结构，便于定制和扩展。

## 硬件

WowSkin 的硬件设计为 **专有**，未包含在此开源仓库中。如果您对 WowSkin 硬件感兴趣，请联系我们或访问我们的 [官方商店](https://item.taobao.com/item.htm?ft=t&id=863972140022)。

### 支持的硬件

WowSkin 旨在与我们专有的硬件无缝配合使用，包括：

- 预校准的磁传感器阵列。
- 高性能数据采集模块。
- 即插即用的兼容连接器。

如果您选择使用其他硬件，可能需要对代码进行一些修改。

## 安装

### 环境要求

- Python 3.8 或更高版本


## **安装方法**

1. **克隆此仓库：**
   ```bash
   git clone https://github.com/WowRobo-Robotics/WowSkin.git --recursive
   ```

3. **安装项目：**
   
   ```bash
   pip install -e .
   ```

---

## **快速使用指南**

1. **硬件连接**
   - 使用 QWIIC 电缆将磁力计电路板与微控制器连接。
   - 将电路板插入设备槽位，然后将皮肤覆盖在 3D 打印的顶端。

2. **检测 COM 端口**
   - 确认您的微控制器连接到的设备路径（`<port>`），具体步骤如下：
     - **Linux**: `ls /dev/ | grep -e ACM -e USB`
     - **MacOS**: `ls /dev/ | grep cu.usb`
     - **Windows**: 打开设备管理器并查看 "端口(COM & LPT)"。

3. **运行可视化工具**
   使用以下命令运行可视化工具：
   ```bash
   python wowskin_viz.py -p <port>
   ```

4. **重新校准零点**
   由于传感器测量可能会随时间漂移，您可以在可视化过程中按下 `B` 键重新校准。

---

## **功能亮点**

- **实时磁场感知**：高精度采集 XYZ 方向的磁场变化。
- **模块化设计**：支持多种使用场景的扩展和定制。
- **跨平台支持**：兼容 Windows、Linux 和 MacOS 操作系统。
- **可视化工具**：内置实时可视化功能，便于快速调试和演示。

---

## **Credits**

WowSkin 的开发基于以下开源项目：
- [AnySkin](https://any-skin.github.io)：提供了核心的磁场传感技术和软件架构。
- [ReSkin](https://reskin.dev)：提供了模块化传感器集成和触觉反馈的设计理念。

---

## **许可证**

WowSkin 使用 [MIT License](LICENSE) 许可证开源软件部分。  
硬件设计为专有内容，未包含在开源范围内。如需了解更多或购买硬件，请访问我们的 [官方商店](https://yourstore.com)。

