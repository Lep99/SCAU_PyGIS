# -*- coding: UTF-8 -*-
# ==============================================
# File   : Choropleth_Map.py
# IDE    : PyCharm
# Author : wenhauLee
# Date   : 2020/5/12 21:31
# Desc   : 制作等值区域图
# ==============================================

from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
# 声明输入输出文件
in_fn = r'D:\FileRecv\GIS开发新技术\第2-4章例子\Lecture02\2_GDAL_Raster\elevation.tif'
# 以只读模式打开输入文件，构建数据集
in_ds = gdal.Open(in_fn,0)
# 获取dem的唯一波段
in_band = in_ds.GetRasterBand(1)
# 对波段进行统计
in_band.FlushCache()
# 列数为XSize，打印输入栅格行列数、最大最小值、数据类型
minVal = in_band.GetMinimum()
maxVal = in_band.GetMaximum()
rows = in_band.YSize
cols = in_band.XSize
# 以浮点型数组形式读取输入栅格数据
in_data = in_ds.ReadAsArray(0,0,cols,rows).astype(np.float)
# 构建输出栅格数组
out_data = np.ones(dtype= float,shape=(rows,cols))
# 将输入栅格值转为ScaleFactor，为方便计算*1000
for row in range(in_ds.RasterYSize):
    for col in range(in_ds.RasterXSize):
        out_data[row,col] = 1000*((in_data[row,col] - minVal)/(maxVal - minVal))
# print(out_data)
# 开始进行绘图
plt.figure()
# 分为五百级，红白渐变
CT=plt.contourf(out_data,500,cmap=plt.cm.Reds_r)
plt.colorbar(CT)
plt.show()
# 关闭输入栅格
in_ds = None
out_data = None
print("高程等值区域图绘制完毕！")
