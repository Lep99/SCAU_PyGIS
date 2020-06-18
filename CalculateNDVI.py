# -*- coding: UTF-8 -*-
# ==============================================
# File   : CalculateNDVI.py
# IDE    : PyCharm
# Author : wenhauLee
# Date   : 2020/5/22 15:31
# Desc   : Lab1 使用Python的GDAL模块，基于所提供的Landsat遥感数据计算NDVI（归一化植被指数）
# ==============================================

from osgeo import gdal
import numpy as np
import os
# 相关文件全路径
b40_fn = r'D:\FileRecv\GIS开发新技术\实验课材料\实验一\landsat\L71026029_02920000609_B40_CLIP.TIF'
b30_fn = r'D:\FileRecv\GIS开发新技术\实验课材料\实验一\landsat\L71026029_02920000609_B30_CLIP.TIF'
ndvi_fn = r'D:\FileRecv\GIS开发新技术\实验课材料\实验一\landsat\NDVI.TIF'

# 打开Band4，Band3
b40_ds = gdal.Open(b40_fn)
b30_ds = gdal.Open(b30_fn)

# 判断文件夹中是否有数据及结果文件
if b40_ds is None or b30_ds is None:
    print("文件未找到！")
# 将原有生成结果文件删除
if os.path.exists(ndvi_fn):
    os.remove(ndvi_fn)

#设置输出文件驱动与输入文件相同
ndviDriver = b40_ds.GetDriver()
ndvi_ds = ndviDriver.CreateCopy(ndvi_fn,b40_ds,0)
# 获取波段值
b40_band = b40_ds.GetRasterBand(1)
b30_band = b30_ds.GetRasterBand(1)
# 波段统计
b40_band.FlushCache()
b30_band.FlushCache()
# 获取栅格行列数
rows = b40_band.YSize
cols = b40_band.XSize
# Band4，3的栅格数组
b40_data = b40_ds.ReadAsArray(0,0,cols,rows).astype(np.float)
b30_data = b30_ds.ReadAsArray(0,0,cols,rows).astype(np.float)
# 构建输出栅格数组
ndvi_data = np.ones(dtype= float,shape=(rows,cols))
# 计算NDVI
for row in range(b40_ds.RasterYSize):
    for col in range(b40_ds.RasterXSize):
        ndvi_data[row, col] = float((b40_data[row, col] - b30_data[row, col]) / (b40_data[row, col] + b30_data[row, col]))
print(ndvi_data)
# 将NDVI写入栅格文件
ndvi_band = ndvi_ds.GetRasterBand(1)
ndvi_band.WriteArray(ndvi_data.astype(np.float))
# 关闭文件
b40_ds = None
b30_ds = None
ndvi_ds = None












