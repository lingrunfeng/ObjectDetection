# 训练与验证指导（YOLOv8 + ROS2）

本指南覆盖：数据准备、数据验证、训练模型、获取模型文件、在 ROS2 中加载并验证模型、常见问题与调试方法。

**环境假设**
- 项目根目录：`/home/student26/ObjectDetection`
- 数据集目录：`/home/student26/ObjectDetection/dataset`
- 已安装 Python3、`pip`、以及必要的 ROS2 环境并且已 `source install/setup.bash`（若使用 workspace）。

**快速概览**
1. 准备并验证数据集（YOLO 格式）
2. 运行训练脚本生成 `best.pt`
3. 在 ROS 节点中使用模型并验证检测结果


**1. 数据准备（必须）**
- 数据目录（参见 `dataset/data.yaml`）：
  - `path: /home/student26/ObjectDetection/dataset`
  - `train: images/train`
  - `val: images/val`
- 类别信息：`dataset/classes.txt` 与 `dataset/data.yaml` 的 `names` 必须顺序一致。
- 标签格式：YOLO txt，每行 `class x_center y_center width height`（坐标归一化，0~1）。标签文件与图片同名。
- 注意目录拼写（工作区中可能出现 `labels` 与 `lables`）：请确保正确为 `dataset/labels/...`。

快速检查示例（在项目根目录）：
```bash
ls -la dataset/images/train dataset/images/val
ls -la dataset/labels/train dataset/labels/val
cat dataset/classes.txt
```
如果你的标签在 `dataset/lables`：
```bash
mkdir -p dataset/labels
mv dataset/lables/* dataset/labels/ || true
```


**2. 验证数据集（强烈建议）**
项目包含 `dataset/verify_dataset.sh`，先运行它：
```bash
bash dataset/verify_dataset.sh
```
该脚本会检查图片与标签配对、类别索引、以及基本格式问题。若报错，根据提示修复对应图片或标签。


**3. 安装依赖（最小）**
建议创建虚拟环境并安装：
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install ultralytics opencv-python
# 若需 GPU，请安装与 CUDA 对应的 torch:
# pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cuXXX
```
如果打算使用 OpenVINO 加速（可选）：
```bash
pip install openvino-dev
```


**4. 训练模型（生成 `best.pt`）**
项目包含训练脚本：`dataset/train_yolo.py` 与快速脚本 `dataset/start_training.sh`。

- 运行（推荐先运行验证脚本）：
```bash
# 先切到项目根
cd /home/student26/ObjectDetection
# 使用快速脚本（会先 run verify，再训练）
bash dataset/start_training.sh
# 或直接运行训练脚本
python3 dataset/train_yolo.py
```
- 默认训练参数（在脚本中）：
  - 基础模型：`yolov8n.pt`（可改为 `yolov8s.pt` 等）
  - epochs: `100`
  - imgsz: `640`
  - batch: `16`（如 GPU 内存不足，请减小）
  - name: `blocks_detection`（结果目录 `runs/detect/blocks_detection/`）

训练结束后：
- 最佳模型：`runs/detect/blocks_detection/weights/best.pt`
- 最后一轮模型：`runs/detect/blocks_detection/weights/last.pt`


**5. （可选）导出为 OpenVINO**
`yolov8_node` 支持自动导出 OpenVINO（若 `use_openvino` 为 `True`，且系统已装 OpenVINO）。导出也可以手动完成：
```python
from ultralytics import YOLO
model = YOLO('runs/detect/blocks_detection/weights/best.pt')
model.export(format='openvino')
# 导出后会生成目录： runs/detect/blocks_detection/weights/best_openvino_model/ 或类似路径
```
节点会寻找 `<basename>_openvino_model/` 目录来加载 OpenVINO 模型。


**6. 在 ROS2 中部署与验证**
节点实现文件：`src/yolov8_ros2/yolov8_ros2/yolov8_node.py`。
主要参数：
- `model`: 模型路径，默认 `yolov8n.pt`（launch 文件可覆盖）
- `device`: `cpu` 或 `cuda:0`
- `use_openvino`: `true/false`

推荐方式：使用 `camera_yolo.launch.py` 同时启动相机与 YOLO 节点，并通过 launch 参数指定你的 `best.pt`：

在启动前，请确保：
- 已构建并 source 工作区（例如 `source install/setup.bash`）
- 如果使用 Realsense，确保 `realsense2_camera` 包已安装且可用

启动命令示例：
```bash
第一步：设置环境并启动
Launch 文件已自动配置为使用你的自定义模型 blocks_yolov8n.pt。

cd /home/student26/ObjectDetection
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch yolov8_ros2 camera_yolo.launch.py

第二步：打开 Rviz2 查看结果
在另一个终端运行：
cd /home/student26/ObjectDetection
source /opt/ros/jazzy/setup.bash
source install/setup.bash
rviz2

```
如果只想启动 yolov8 节点（不包含相机）：
```bash
ros2 launch yolov8_ros2 yolo.launch.py model:=/home/student26/ObjectDetection/runs/detect/blocks_detection/weights/best.pt device:=cpu use_openvino:=false
```

节点会订阅：
- `/camera/camera/color/image_raw`

节点会发布：
- 带框的结果图像：`/yolo/prediction/image`（sensor_msgs/Image）
- 检测字典：`/yolo/prediction/item_dict`（std_msgs/String，内容为 JSON）

查看检测输出：
```bash
# 查看 JSON 检测信息
ros2 topic echo /yolo/prediction/item_dict
# 使用 GUI 查看带框图像
ros2 run rqt_image_view rqt_image_view
# 在 rqt_image_view 中选择 /yolo/prediction/image
```


**7. 常见问题与排查**
- 无法找到标签/类别错位：检查 `dataset/data.yaml` 的 `names` 与 `dataset/classes.txt` 顺序一致。
- GPU 内存不足：减小 `batch` 或 `imgsz`，或使用更小模型（`yolov8n`）。
- ROS 节点报错找不到模型：确认在 launch 命令中 `model:=<绝对路径>`，或把模型复制到项目根并在 launch 中修改 `MODEL_PATH`。
- OpenVINO 导出失败：先确保 `openvino-dev` 安装且环境变量配置正确，或在 launch 中将 `use_openvino:=false`。
- 相机话题不存在：确认相机驱动已启动并发布 `/camera/camera/color/image_raw`，用 `ros2 topic list` 检查。


**8. 建议工作流**
- 开发与调试阶段用 CPU 进行小规模训练或少量 epoch 快速验证标签是否正确。
- 确认数据与标签无误后，用合适的模型尺寸与合适的 batch、更多 epoch 在 GPU 上训练以获得更高精度。
- 训练完成后优先使用 `best.pt` 在 ROS 上测试，若需要加速再考虑导出为 OpenVINO 并在节点中开启加速。


---
如果你希望，我可以：
- 1) 代为运行 `bash dataset/verify_dataset.sh` 并把输出贴上来；
- 2) 修改 `camera_yolo.launch.py` 中的 `MODEL_PATH` 为训练好的 `best.pt` 并提交补丁；
- 3) 帮你启动一个本地的训练（如果你允许我在工作区执行命令）。

告诉我下一步你想我做哪项。