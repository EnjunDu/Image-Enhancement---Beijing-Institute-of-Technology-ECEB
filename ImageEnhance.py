import numpy as np
from PIL import Image

def Nearest_Neighbour_Interpolation(image,new_height,new_width):
    height,width = image.shape[:2] #获取原始图像的尺寸
    new_image = np.zeros((new_height,new_width,3),dtype=np.uint8)#创建新图像
    for i in range(new_height):
        for j in range(new_width):
            x = i*(height/new_height)#计算x,y在原始图像中的坐标
            y = j *(width/new_width)
            x1,y1 =int(round(x,0)),int(round(y,0)) #找到最近的像素点坐标
            # 确保坐标不超出原始图像的边界
            x1 = min(max(x1, 0), height - 1)
            y1 = min(max(y1, 0), width - 1)
            new_pixel = image[x1,y1]#该步骤和下一步骤使用最近邻插值获取新像素值
            new_image[i,j] = new_pixel.astype(np.uint8)#.astype(np.uint8)将浮点数值转换为8位无符号整数类型

    return new_image

def Bilinear_Interpolation(image,new_height,new_width):
    height,width = image.shape[:2] #获取原始图像的尺寸
    new_image = np.zeros((new_height,new_width,3),dtype=np.uint8)#创建新图像
    for i in range(new_height):
        for j in range(new_width):
            x = i*(height/new_height)#计算x,y在原始图像中的坐标
            y = j *(width/new_width)
            x1,y1 = int(x),int(y)#找到最近的四个像素坐标
            x1 = min(max(x1, 0), height - 1)
            y1 = min(max(y1, 0), width - 1)#防止坐标超出画面边界
            x2,y2 = min(x1+1,height -1),min(y1+1,width -1)

            dx,dy = x-x1,y-y1 #计算其所占的权重
            #使用双线性插值计算像素值
            "'(1 - dx) 和 (1 - dy) 分别表示新像素点与 (x1, y1) 最近的像素点在水平和垂直方向上的距离比例\
             (dx * (1 - dy)) 表示新像素点与 (x2, y1)最近的像素点在水平方向上的距离比例，同时在垂直方向上与(x1, y1)最近的像素点的距离比例。\
            ((1 - dx) * dy)表示新像素点与(x1, y2)最近的像素点在水平方向上的距离比例，同时在垂直方向上与(x1, y1)最近的像素点的距离比例。\
            (dx * dy)表示新像素点与(x2, y2)最近的像素点在水平方向上的距离比例，同时在垂直方向上与(x1, y1)最近的像素点的距离比例。'"
            #四个权重组合使得过度更平滑
            new_pixel=(1-dx)*(1-dy)*image[x1,y1]+dx*(1-dy)*image[x2,y1]+(1-dx)*dy*image[x1,y2]+dx*dy*image[x2,y2]
            new_image[i, j] = new_pixel.astype(np.uint8)

    return new_image

def main():
    print("请选择图片插值方法：")
    print("输入1为最近邻插值法")
    print("输入2为双线性插值法")
    choice = input()
    input_image = np.array(Image.open("test.png"))

    # 获取用户输入的新的高度和宽度
    new_height = input_image.shape[0]*int(input("请输入新的高度（输入倍数）（只能输入纯整数）: "))
    new_width = input_image.shape[1] *int(input("请输入新的宽度（输入倍数）（只能输入纯整数）:"))

    if choice == "1":
        scaled_image = Nearest_Neighbour_Interpolation(input_image,new_height,new_width)
        Image.fromarray(scaled_image).save("Nearest_Neighbour_Interpolation_Image.png")
    if choice =="2":
        scaled_image = Bilinear_Interpolation(input_image,new_height,new_width)
        Image.fromarray(scaled_image).save("Bilinear_Interpolation_Image.png")
    print("处理完成")

if  __name__ =="__main__":
    main()
