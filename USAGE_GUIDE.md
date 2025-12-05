# YOLOv8 ROS2 使用指南

## 🎯 如何查看检测结果

### 方法1: 使用 Rviz2 可视化（推荐）

#### 步骤1: 启动YOLOv8节点（已在运行）
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch yolov8_ros2 camera_yolo.launch.py
```

#### 步骤2: 在另一个终端打开 Rviz2
```bash
source /opt/ros/jazzy/setup.bash
rviz2
```

#### 步骤3: 在Rviz2中配置显示

1. **设置Fixed Frame**:
   - 在左侧面板找到 "Global Options"
   - 将 "Fixed Frame" 从 `map` 改为 `camera_link`

2. **添加图像显示**:
   - 点击左下角 "Add" 按钮
   - 选择 "Image" 类型
   - 点击 "OK"
   - 在 "Image" 面板中，设置 "Image Topic" 为: `/yolo/prediction/image`
   - 现在应该能看到带检测框和分割结果的图像

3. **（可选）添加原始相机图像**:
   - 再次点击 "Add" → "Image"
   - 设置 "Image Topic" 为: `/camera/color/image_raw`
   - 可以看到原始RGB图像

4. **（可选）添加点云显示**:
   - 点击 "Add" → "PointCloud2"
   - 设置 "Topic" 为: `/camera/depth/color/points`
   - 可以看到3D点云

### 方法2: 使用 rqt_image_view（简单快速）

在另一个终端运行：
```bash
source /opt/ros/jazzy/setup.bash
rqt_image_view
```

然后在下拉菜单中选择话题：`/yolo/prediction/image`

### 方法3: 查看检测结果数据

查看JSON格式的检测结果：
```bash
source /opt/ros/jazzy/setup.bash
ros2 topic echo /yolo/prediction/item_dict
```

这会显示检测到的物体信息，包括：
- 物体类别（class）
- 物体位置（position，3D坐标）

## 📊 应该看到什么

### 在 `/yolo/prediction/image` 话题中：
- **彩色图像**，带有：
  - YOLOv8检测框（边界框）
  - 分割掩码（segmentation masks）
  - 类别标签和置信度
  - 背景已被移除（超过深度阈值的区域显示为灰色）

### 在控制台输出中：
- 应该看到类似这样的日志：
  ```
  [yolov8_node-2] Yolo detected items: ['person', 'bottle', ...]
  ```
  显示检测到的物体类别列表

## 🔍 可用的ROS2话题

运行以下命令查看所有话题：
```bash
ros2 topic list
```

主要话题：
- `/yolo/prediction/image` - YOLOv8检测结果图像（带检测框和分割）
- `/yolo/prediction/item_dict` - JSON格式的检测结果（物体类别和位置）
- `/camera/color/image_raw` - 原始RGB图像
- `/camera/aligned_depth_to_color/image_raw` - 对齐的深度图像
- `/camera/depth/color/points` - 彩色点云

## ⚠️ 常见问题

### 1. NumPy版本警告
如果看到NumPy兼容性警告，不影响使用。如果需要修复：
```bash
pip3 install --break-system-packages "numpy<2"
```

### 2. 没有检测到物体
- 确保相机正对物体
- 检查光照条件
- 查看控制台是否有 "Yolo detected items" 日志

### 3. 图像不更新
- 检查相机是否正常工作
- 运行 `ros2 topic hz /yolo/prediction/image` 查看发布频率

## 🎮 快速测试命令

```bash
# 查看话题列表
ros2 topic list

# 查看图像话题的发布频率
ros2 topic hz /yolo/prediction/image

# 查看检测结果
ros2 topic echo /yolo/prediction/item_dict

# 查看话题信息
ros2 topic info /yolo/prediction/image
```


