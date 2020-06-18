# -*- coding: UTF-8 -*-
# ==============================================
# File   : pl_buffer.py
# IDE    : PyCharm
# Author : wenhauLee
# Date   : 2020/5/22 18:15
# Desc   : 使用Python的OGR模块，基于所提供的矢量数据提取新设电线250个地图单位范围内的宗地。
# ==============================================

import sys
from osgeo import ogr

# 打开数据源文件
ds = ogr.Open(r'D:\FileRecv\GIS开发新技术\实验课材料\实验二\data',1)
# 判断文件夹内是否有数据
if ds is None :
    sys.exit('Could not open folder.')
# 打开电力线、宗地图层
powerLine = ds.GetLayer('PowerLine')
parcels = ds.GetLayer('Parcels')
# 若存在先前的结果文件，删除
if ds.GetLayer('pl_buffer'):
    ds.DeleteLayer('pl_buffer')
if ds.GetLayer('intersect_buffer'):
    ds.DeleteLayer('intersect_buffer')
# 构建缓冲区与相交宗地图层，设置其为与宗地图层相同的投影信息，图层类型为面图层
pl_buffer = ds.CreateLayer('pl_buffer',parcels.GetSpatialRef(),ogr.wkbPolygon)
intersect_buffer = ds.CreateLayer('intersect_buffer',parcels.GetSpatialRef(),ogr.wkbPolygon)
# 采用与宗地图层相同的图层描述
pl_buffer_defn = parcels.GetLayerDefn()
intersect_defn = parcels.GetLayerDefn
pl_buffer_feat = ogr.Feature(pl_buffer_defn)
intersect_feat = ogr.Feature(pl_buffer_defn)
print(ogr.GeometryTypeToName(pl_buffer.GetGeomType()))

#  生成电力线的250缓冲区
for pl_feat in powerLine:
    buff_geom = pl_feat.geometry().Buffer(250)
    pl_buffer_feat.SetGeometry(buff_geom)
    # 将生成缓冲区字段与电力线保持一致，确保其对应性
    for i in range(pl_feat.GetFieldCount()):
        value = pl_feat.GetField(i)
        pl_buffer_feat.SetField(i, value)
    pl_buffer.CreateFeature(pl_buffer_feat)

#  将生成缓冲区与宗地相交
for parcels_feat in parcels:
    pl_buffer_geom = pl_buffer_feat.geometry()
    buff_geom2 = parcels_feat.geometry().Intersection(pl_buffer_geom)
    intersect_feat .SetGeometry(buff_geom2)
    # 将相交区域字段与原图层保持一致，确保其对应性
    for i in range(parcels_feat.GetFieldCount()):
        value = parcels_feat.GetField(i)
        parcels_feat.SetField(i, value)
    intersect_buffer.CreateFeature(intersect_feat)

ds = None




