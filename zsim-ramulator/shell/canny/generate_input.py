import os
import random
import shutil

def select_random_images(src_dir, dst_dir, num_images=100):
    # 获取目录中的所有文件
    all_files = [f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]
    
    # 过滤出所有的图片文件（假设图片文件扩展名为 .jpg, .jpeg, .png）
    image_files = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # 如果图片数量不足，调整数量
    num_images = min(num_images, len(image_files))
    
    # 随机选择指定数量的图片
    selected_images = random.sample(image_files, num_images)
    
    # 确保目标目录存在
    os.makedirs(dst_dir, exist_ok=True)
    
    # 复制图片到目标目录，并按顺序重命名
    for idx, image in enumerate(selected_images):
        src_path = os.path.join(src_dir, image)
        dst_path = os.path.join(dst_dir, "{}.jpg".format(idx))
        shutil.copy(src_path, dst_path)
    
    print("Selected and copied {} images to {}".format(num_images, dst_dir))

if __name__ == "__main__":
    src_directory = "/root/ramulator-pim/zsim-ramulator/shell/canny/cifar-10/cifar-10/train/cat/"
    dst_directory = "/root/ramulator-pim/zsim-ramulator/shell/canny/input"
    
    group_size = 2000
    select_random_images(src_directory, dst_directory, num_images=group_size)
