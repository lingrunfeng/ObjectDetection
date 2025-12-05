# YOLOv8 ROS2 运行指南

## 📁 工作空间结构

```
/home/student26/ObjectDetection/
├── src/
│   └── yolov8_ros2/          # ROS2包源码
├── install/                   # 安装目录（构建后生成）
├── build/                     # 构建目录（构建后生成）
└── log/                       # 日志目录（构建后生成）
```

## 🚀 快速开始

### 步骤1: 设置环境变量（每次新终端都需要）

```bash
# 进入工作空间
cd /home/student26/ObjectDetection

# 设置ROS2环境
source /opt/ros/jazzy/setup.bash

# 设置工作空间环境
source install/setup.bash
```

**提示**: 可以将这些命令添加到 `~/.bashrc` 中自动加载：
```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
echo "source /home/student26/ObjectDetection/install/setup.bash" >> ~/.bashrc
```

### 步骤2: 运行YOLOv8 + Realsense相机

```bash
ros2 launch yolov8_ros2 camera_yolo.launch.py
```

这会启动：
- Realsense相机节点（发布RGB和深度图像）
- YOLOv8检测节点（进行物体检测和分割）

### 步骤3: 查看检测结果

#### 方法A: 使用 rqt_image_view（最简单）

在**另一个终端**运行：
```bash
cd /home/student26/ObjectDetection
source /opt/ros/jazzy/setup.bash
source install/setup.bash
rqt_image_view
```

在下拉菜单中选择话题：`/yolo/prediction/image`

#### 方法B: 使用 Rviz2（功能更全）

在**另一个终端**运行：
```bash
cd /home/student26/ObjectDetection
source /opt/ros/jazzy/setup.bash
source install/setup.bash
rviz2
```

在Rviz2中：
1. 设置 Fixed Frame 为 `camera_link`
2. 点击 "Add" → 选择 "Image"
3. 设置 Image Topic 为 `/yolo/prediction/image`

## 📊 可用的Launch文件

### 1. camera_yolo.launch.py（完整功能）
启动相机 + YOLOv8检测
```bash
ros2 launch yolov8_ros2 camera_yolo.launch.py
```

### 2. yolo.launch.py（仅YOLOv8节点）
如果已经有其他相机节点在运行，可以只启动YOLOv8：
```bash
ros2 launch yolov8_ros2 yolo.launch.py
```

### 3. camera.launch.py（仅相机）
如果只需要相机，不运行YOLOv8：
```bash
ros2 launch yolov8_ros2 camera.launch.py
```

## 📡 ROS2话题

### 主要话题：

| 话题名称 | 类型 | 说明 |
|---------|------|------|
| `/yolo/prediction/image` | `sensor_msgs/Image` | YOLOv8检测结果图像（带检测框和分割） |
| `/yolo/prediction/item_dict` | `std_msgs/String` | JSON格式的检测结果（物体类别和3D位置） |
| `/camera/camera/color/image_raw` | `sensor_msgs/Image` | 原始RGB图像 |
| `/camera/camera/aligned_depth_to_color/image_raw` | `sensor_msgs/Image` | 对齐的深度图像 |
| `/camera/depth/color/points` | `sensor_msgs/PointCloud2` | 彩色点云 |

注意：由于相机节点配置原因，原始图像话题可能带有双重 `camera` 前缀（如 `/camera/camera/...`）。YOLO节点已配置为自动适应此话题。

### 查看所有话题：
```bash
ros2 topic list
```

### 查看话题数据：
```bash
# 查看检测结果
ros2 topic echo /yolo/prediction/item_dict

# 查看话题信息
ros2 topic info /yolo/prediction/image

# 查看发布频率
ros2 topic hz /yolo/prediction/image
```

## 🔧 重新构建

如果修改了代码，需要重新构建：

```bash
cd /home/student26/ObjectDetection
colcon build --symlink-install
source install/setup.bash
```

## ⚙️ 参数配置

可以在launch文件中修改参数，或者使用命令行参数：

```bash
# 指定使用CPU（默认自动检测GPU）
ros2 launch yolov8_ros2 camera_yolo.launch.py device:=cpu

# 指定使用GPU
ros2 launch yolov8_ros2 camera_yolo.launch.py device:=cuda:0
```

## 🐛 故障排除

### 1. 找不到包
```bash
# 确保环境已设置
source /opt/ros/jazzy/setup.bash
source /home/student26/ObjectDetection/install/setup.bash

# 验证包是否存在
ros2 pkg list | grep yolov8
```

### 2. 相机未检测到
- 确保相机连接到USB 3.0端口（蓝色接口）
- 检查相机是否被识别：`lsusb | grep Intel`
- 查看相机节点日志

### 3. 没有检测结果
- 检查控制台是否有 "Yolo detected items" 日志
- 确保相机正对物体
- 检查光照条件

### 4. NumPy版本警告
如果看到NumPy兼容性警告，可以降级NumPy：
```bash
pip3 install --break-system-packages "numpy<2"
```

## 📝 预期输出

### 控制台输出应该看到：

```
[INFO] [realsense2_camera_node-1]: RealSense ROS v4.56.4
[INFO] [realsense2_camera_node-1]: Device with serial number ... was found.
[INFO] [realsense2_camera_node-1]: RealSense Node Is Up!
[yolov8_node-2] YOLOv8s-seg summary: 85 layers, 11,810,560 parameters
[yolov8_node-2] Yolo detected items: ['person', 'bottle', ...]
```

### 在图像中应该看到：
- 彩色图像
- 物体检测框（边界框）
- 分割掩码（物体轮廓）
- 类别标签
- 背景已移除（远处物体为灰色）

## 🎯 下一步

1. **查看检测结果数据**：
   ```bash
   ros2 topic echo /yolo/prediction/item_dict
   ```

2. **保存检测结果图像**（使用rqt_image_view的保存功能）

3. **集成到你的应用**：订阅 `/yolo/prediction/item_dict` 话题获取检测结果

4. **调整参数**：修改 `yolov8_node.py` 中的阈值和参数



