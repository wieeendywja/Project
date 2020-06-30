import numpy as np
import cv2

filename = "input.jpg"  # 原图像文件名
rectangle = (0, 0, 1, 1)
rectangle_color = [203, 192, 255]  # 设置矩形框颜色为粉色
draw = False
image = cv2.imread(filename)
image2 = image.copy()


def draw_rectangle(mouse, x, y, flags, param):
    global rectangle, initial_x, initial_y, draw, image

    # 在目标外画一个框，从而进行分割
    if mouse == cv2.EVENT_LBUTTONDOWN:
        draw = True
        initial_x = x
        initial_y = y
    elif mouse == cv2.EVENT_MOUSEMOVE:
        if draw == True:
            image = image2.copy()
            cv2.rectangle(image, (initial_x, initial_y), (x, y), rectangle_color, 2)
            rectangle = (initial_x, initial_y, abs(initial_x - x), abs(initial_y - y))
    elif mouse == cv2.EVENT_LBUTTONUP:
        draw = False
        cv2.rectangle(image, (initial_x, initial_y), (x, y), rectangle_color, 2)
        rectangle = (initial_x, initial_y, abs(initial_x - x), abs(initial_y - y))


if __name__ == "__main__":
    mask = np.zeros(image.shape[:2], dtype=np.uint8)  # 初始化mask
    output = np.zeros(image.shape, np.uint8)
    cv2.namedWindow('input')
    cv2.namedWindow('output')
    cv2.setMouseCallback('input', draw_rectangle)  # 鼠标响应

    while True:
        cv2.imshow('output', output)
        cv2.imshow('input', image)
        key = 0xFF & cv2.waitKey(1) # 等待键盘输入

        if key == 27:  # ESC
            break
        elif key == ord('c'):  # 分割图像
            bgdmodel = np.zeros((1, 65), np.float64)
            fgdmodel = np.zeros((1, 65), np.float64)
            cv2.grabCut(image2, mask, rectangle, bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_RECT)
        elif key == ord('s'):  #储存图像
            cv2.imwrite('output.jpg', output)
        result_mask = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')
        output = cv2.bitwise_and(image2, image2, mask=result_mask)

    cv2.destroyAllWindows()
