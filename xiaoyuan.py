import os
import ddddocr
from time import sleep
from PIL import Image
last_text = None
last_comp_flag = -1
def take_screenshot(path):
    """从设备截取屏幕并保存到指定路径。"""
    os.system(f'adb shell screencap -p > {path}')
 
    # 读取截取的屏幕截图并替换行结束符
    with open(path, 'rb') as f:
        return f.read().replace(b'\r\n', b'\n')
 
def process_image(image_path, crop_area):
    """打开图片，裁剪并返回裁剪后的图片。"""
    with Image.open(image_path) as img:
        return img.crop(crop_area)
 
def extract_text(img_bytes):
    """提取图片中的文本。"""
    # with open(img, 'rb') as f:
    #     img_bytes = f.read()
    res = ocr.classification(img_bytes)
    return res.replace(' ', '').replace('\n', '')
 
def compare_numbers(x, y):
    """比较两个数字并相应地执行滑动操作。"""
    try:
        x_int, y_int = int(x), int(y)
        if x_int > y_int:
            print(f"{x} > {y}")
            os.system("adb shell input swipe 1300 700 1540 900 30")
            os.system("adb shell input swipe 1540 900 1300 1100 30")
            # os.system("adb shell input swipe 1210 920 1200 930 30")
        else:
            print(f"{x} < {y}")
            os.system("adb shell input swipe 1540 700 1300 900 30")
            os.system("adb shell input swipe 1300 900 1540 1100 30")
            # os.system("adb shell input swipe 1210 920 1200 930 30")
        return True
    except ValueError:
        print("数字格式无效。")
        return False

def main():
    """主程序逻辑。"""
    global last_text, last_comp_flag
    screenshot_path = 'screenshot.png'
 
    # 截取屏幕并保存
    screenshot = take_screenshot(screenshot_path)
    with open(screenshot_path, 'wb') as f:
        f.write(screenshot)
 
    # 定义裁剪区域（左，上，右，下）分别是两个数字在图片中的区域坐标
    crop_areas = [
        (1170, 376, 1250, 430),
        (1330, 376, 1410, 430)
    ]
 
    cropped_images = []
    for i, crop_area in enumerate(crop_areas, start=1):
        cropped_image = process_image(screenshot_path, crop_area)
        # cropped_image_path = f"screenshot{i}.png"
        # cropped_image.save(cropped_image_path)
        cropped_images.append(cropped_image)
 
    # 从裁剪后的图片中提取文本
    texts = [extract_text(image) for image in cropped_images]
    if (last_comp_flag == 1) and (texts == last_text):
        return
    # 比较提取的数字
    comp_res = compare_numbers(texts[0], texts[1])
    # if not comp_res:
    #     last_comp_flag = -1
    # else:
    #     if last_comp_flag == -1:
    #         last_comp_flag = 0
    #     else:
    #         if texts != last_text:
    #             last_comp_flag = 1
    # print(last_comp_flag)
    # last_text = texts

 
 
if __name__ == '__main__':
    ocr = ddddocr.DdddOcr(show_ad=False)
    while True:
        main()
        # os.system("adb shell input swipe 1540 700 1300 900 30")
        # os.system("adb shell input swipe 1300 900 1540 1100 30")
        # os.system("adb shell input swipe 1540 1100 1300 1300 30")
        sleep(0.15)