'''艺术签名生成器'''
import os
import re
import io
import sys
import requests
from PIL import Image
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
'''背景音乐'''
import pygame
file=r'F:\艺术签名生成器\bb.mp3'
pygame.mixer.init()
track = pygame.mixer.music.load(file)
pygame.mixer.music.play(-1)

class ArtSignGenerator(QWidget):
    def __init__(self, parent=None):
        super(ArtSignGenerator, self).__init__(parent)
        self.setFixedSize(600, 500)
        self.setWindowTitle('艺术签名生成器-TONOW')
        self.setWindowIcon(QIcon('resource/icon/icon.jpg'))
        self.grid = QGridLayout()
        # 定义一些必要的组件
        # --label
        self.show_label = QLabel()
        self.show_label.setScaledContents(True)
        self.show_label.setMaximumSize(600, 400)
        self.show_image = Image.open('resource/image/ori.jpg').convert('RGB')
        self.show_image1 = Image.open('resource/image/ori.jpg').convert('RGB')
        self.updateimage()
        self.show_image_ext = 'jpg'
        self.show_image_ext1 = 'jpg'
        self.name_label = QLabel('输入您的姓名:')
        self.font_label = QLabel('艺术签名字体:')
        self.color_label = QLabel('艺术签名颜色:')
        self.background_label = QLabel('艺术签名颜色背景:')
        # --输入框
        self.name_edit = QLineEdit()
        self.name_edit.setText('签名生成器')
        # --button
        self.generate_button = QPushButton('生成艺术签名')
        self.save_button = QPushButton('保存艺术签名')
        # --下拉框
        self.font_combobox = QComboBox()
        for item in ['一笔艺术签', '连笔商务签', '一笔商务签', '真人手写', '暴躁字','黑体','楷体','仿宋','行楷','雁翔','行楷繁',
                     '舒同','古文篆书','繁中变','隶书','隶书繁','仿宋体','秀英','双线','空心繁','雪峰','花蝶','彩蝶','飞翔',
                     '萝卜文','火柴文','黛玉字体','嘟嘟字','凌波字体','清韵字体','水波文字','萝莉字','空心体','明星手写体','签名字体',
                     '草书体','手写字','行书','连笔草书','连笔草字','猫猫字体','情书常规体','倾倒特效手写',
                     '垂直特效手写','水平特效手写','三十度角仰望天','四十五度角仰望','娃娃体','手写体','静心楷体','硬笔行书','手写文字',
                     '肥圆手写','钢笔体','书法字体','天真娃娃体','太极体','钢笔字','和楷体','灵芝体','鼠标体','硬草书','小丸子',
                     '大草体字','连笔艺术字','连笔手写字','毛泽东字体','一起去看海','一起恋爱','万圣节快乐','他夏了夏天',
                     '你最疼爱的人','信心相随','单翼雪蝶','南辞遇蝶','卷卷爱红唇','后会有期','咯咯哒的梦想','圈圈泡泡','地狱引路人',
                     '夏天的风','安静的美女子','小兔闹革命','小肥泡中文','幸福四叶草','开开的蛋糕','恋爱写真','恋爱蝴蝶结','恬夕别乱',
                     '恬夕恋夕','恰逢其会','星心甜甜圈','星火爱情','星际Cream','春田小蜜蜂','暮夏何其孽','梦中的婚礼','玉米荡漾',
                     '甜菜五道杠','绿光森林','花俏公主','钢笔楷书','花里胡哨','草莓之心','茶蘼花开','蝴蝶结云彩','蝶恋之樱','迪斯尼美丽',
                     '阿苗笑笑','佳丽体','马卡龙']:
            self.font_combobox.addItem(item)
        self.color_combobox = QComboBox()
        for item in ['黑色', '蓝色', '红色', '绿色', '黄色', '金色', '褐色',
                     '粉色', '深蓝色', '蓝绿色', '橙色', '海贝壳色', '紫色',
                     '桃色', '粉红色', '紫罗兰色', '银色', '巧克力色', '茶色',
                     '火砖色', '粉蓝色']:
            self.color_combobox.addItem(item)
        self.background_combobox = QComboBox()
        for item in ['黑色', '蓝色', '红色', '绿色', '黄色', '金色', '褐色',
                     '粉色', '深蓝色', '蓝绿色', '橙色', '海贝壳色', '紫色',
                     '桃色', '粉红色', '紫罗兰色', '银色', '巧克力色', '茶色',
                     '火砖色', '粉蓝色']:
            self.background_combobox.addItem(item)
        # 组件布局
        self.grid.addWidget(self.show_label, 0, 0, 5, 5)
        self.grid.addWidget(self.name_label, 5, 0, 1, 1)
        self.grid.addWidget(self.name_edit, 5, 1, 1, 4)
        self.grid.addWidget(self.font_label, 6, 0, 1, 1)
        self.grid.addWidget(self.font_combobox, 6, 1, 1, 4)
        self.grid.addWidget(self.color_label, 7, 0, 1, 1)
        self.grid.addWidget(self.color_combobox, 7, 1, 1, 4)
        self.grid.addWidget(self.background_label, 8, 0, 1, 1)
        self.grid.addWidget(self.background_combobox, 8, 1 ,1 ,4)
        self.grid.addWidget(self.generate_button, 9, 3, 1, 1)
        self.grid.addWidget(self.save_button, 9, 4, 1, 1)
        self.setLayout(self.grid)
        # 事件绑定
        self.generate_button.clicked.connect(self.generate)
        self.save_button.clicked.connect(self.save)
    '''生成签名'''
    def generate(self):
        font2ids_dict = {
                            '一笔艺术签': ['901', '15'],
                            '连笔商务签': ['904', '15'],
                            '一笔商务签': ['905', '14'],
                            '真人手写': ['343', '14'],
                            '卡通趣圆字': ['397', '14'],
                            '暴躁字': ['380', '14'],
                            '黑体':['330','14'],
                            '楷体':['329','14'],
                            '仿宋':['331','14'],
                            '行楷':['2','14'],
                            '雁翔':['4','14'],
                            '行楷繁':['9','14'],
                            '舒同':['13','14'],
                            '古文篆书':['14','14'],
                            '繁中变':['15','14'],
                            '隶书':['18','14'],
                            '隶书繁':['19','14'],
                            '仿宋体':['20','14'],
                            '秀英':['1','14'],
                            '双线':['10','14'],
                            '空心繁':['11','14'],
                            '雪峰':['12','14'],
                            '花蝶':['301','14'],
                            '彩蝶':['302','14'],
                            '飞翔':['303','14'],
                            '萝卜文':['304','14'],
                            '火柴文':['305','14'],
                            '黛玉字体':['307','14'],
                            '嘟嘟字':['308','14'],
                            '凌波字体':['309','14'],
                            '清韵字体':['310','14'],
                            '水波文字':['311','14'],
                            '萝莉字':['317','14'],
                            '空心体':['384','14'],
                            '明星手写体':['5','14'],
                            '签名字体':['6','14'],
                            '草书体':['7','14'],
                            '手写字':['16','14'],
                            '行书':['17','14'],
                            '连笔草书':['21','14'],
                            '连笔草字':['22','14'],
                            '猫猫字体':['312','14'],
                            '情书常规体':['342','14'],
                            '倾倒特效手写':['344','14'],
                            '垂直特效手写':['345','14'],
                            '水平特效手写':['346','14'],
                            '三十度角仰望天':['347','14'],
                            '四十五度角仰望':['348','14'],
                            '娃娃体':['355','14'],
                            '手写体':['356','14'],
                            '静心楷体':['357','14'],
                            '硬笔行书':['358','14'],
                            '手写文字':['359','14'],
                            '肥圆手写':['360','14'],
                            '钢笔体':['363','14'],
                            '书法字体':['385','14'],
                            '天真娃娃体':['386','14'],
                            '太极体':['387','14'],
                            '钢笔字':['388','14'],
                            '和楷体':['389','14'],
                            '灵芝体':['391','14'],
                            '鼠标体':['392','14'],
                            '硬草书':['393','14'],
                            '小丸子':['394','14'],
                            '大草体字':['395','14'],
                            '连笔艺术字':['396','14'],
                            '连笔手写字':['398','14'],
                            '毛泽东字体':['399','14'],
                            '一起去看海':['314','14'],
                            '一起恋爱':['315','14'],
                            '万圣节快乐':['316','14'],
                            '他夏了夏天':['318','14'],
                            '你最疼爱的人':['319','14'],
                            '信心相随':['320','14'],
                            '单翼雪蝶':['321','14'],
                            '南辞遇蝶':['322','14'],
                            '卷卷爱红唇':['323','14'],
                            '后会有期':['324','14'],
                            '咯咯哒的梦想':['325','14'],
                            '圈圈泡泡':['326','14'],
                            '地狱引路人':['327','14'],
                            '夏天的风':['328','14'],
                            '安静的美女子':['332','14'],
                            '小兔闹革命':['333','14'],
                            '小肥泡中文':['334','14'],
                            '幸福四叶草':['335','14'],
                            '开开的蛋糕':['336','14'],
                            '恋爱写真':['337','14'],
                            '恋爱蝴蝶结':['338','14'],
                            '恬夕别乱':['339','14'],
                            '恬夕恋夕':['340','14'],
                            '恰逢其会':['341','14'],
                            '星心甜甜圈':['349','14'],
                            '星火爱情':['350','14'],
                            '星际Cream':['351','14'],
                            '春田小蜜蜂':['352','14'],
                            '暮夏何其孽':['353','14'],
                            '梦中的婚礼':['354','14'],
                            '玉米荡漾':['361','14'],
                            '甜菜五道杠':['362','14'],
                            '绿光森林':['366','14'],
                            '花俏公主':['370','14'],
                            '钢笔楷书':['371','14'],
                            '花里胡哨':['372','14'],
                            '草莓之心':['373','14'],
                            '茶蘼花开':['374','14'],
                            '蝴蝶结云彩':['376','14'],
                            '蝶恋之樱':['377','14'],
                            '迪斯尼美丽':['379','14'],
                            '阿苗笑笑':['381','14'],
                            '佳丽体':['382','14'],
                            '马卡龙':['383','14']
                    }
        color2ids_dict = {
                            '黑色': ['#000000', '#FFFFFF'],
                            '蓝色': ['#0000FF', '#FFFFFF'],
                            '红色': ['#FF0000', '#FFFFFF'],
                            '绿色': ['#00FF00', '#FFFFFF'],
                            '黄色': ['#FFFF00', '#FFFFFF'],
                            '金色': ['#FFD700', '#FFFFFF'],
                            '粉色': ['#FFC0CB', '#FFFFFF'],
                            '深蓝色': ['#00BFFF', '#FFFFFF'],
                            '蓝绿色': ['#00FFFF', '#FFFFFF'],
                            '橙色': ['#FFA500', '#FFFFFF'],
                            '海贝壳色': ['#FFF5EE', '#FFFFFF'],
                            '褐色': ['#A52A2A', '#FFFFFF'],
                            '紫色': ['#800080','#FFFFFF'],
                            '桃色': ['#FFDAB9','#FFFFFF'],
                            '粉红色': ['#FFC0CB', '#FFFFFF'],
                            '紫罗兰色': ['#EE82EE', '#FFFFFF'],
                            '银色': ['#C0C0C0','#FFFFFF'],
                            '巧克力色': ['#D2691E','#FFFFFF'],
                            '茶色': ['#D2B48C','#FFFFFF'],
                            '火砖色': ['#B22222','#FFFFFF'],
                            '粉蓝色': ['#B0E0E6', '#FFFFFF'],
                        }

        background2ids_dict = {
                                '黑色': ['#FFFFFF', '#000000'],
                                '蓝色': ['#FFFFFF', '#0000FF'],
                                '红色': ['#FFFFFF', '#FF0000'],
                                '绿色': ['#FFFFFF', '#00FF00'],
                                '黄色': ['#FFFFFF', '#FFFF00'],
                                '金色': ['#FFFFFF', '#FFD700'],
                                '粉色': ['#FFFFFF', '#FFC0CB'],
                                '深蓝色': ['#FFFFFF', '#00BFFF'],
                                '蓝绿色': ['#FFFFFF', '#00FFFF'],
                                '橙色': ['#FFFFFF', '#FFA500'],
                                '海贝壳色': ['#FFFFFF', '#FFF5EE'],
                                '褐色': ['#FFFFFF', '#A52A2A'],
                                '紫色': ['#FFFFFF', '#800080'],
                                '桃色': ['#FFFFFF', '#FFDAB9'],
                                '粉红色': ['#FFFFFF', '#FFC0CB'],
                                '紫罗兰色': ['#FFFFFF', '#EE82EE'],
                                '银色': ['#FFFFFF', '#C0C0C0'],
                                '巧克力色': ['#FFFFFF', '#D2691E'],
                                '茶色': ['#FFFFFF', '#D2B48C'],
                                '火砖色': ['#FFFFFF', '#B22222'],
                                '粉蓝色': ['#FFFFFF', '#B0E0E6'],
                            }

        url = 'http://www.jiqie.com/a/re14.php'
        headers = {
                    'Referer': 'http://www.jiqie.com/a/14.htm',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/81.0.4044.129 Safari/537.36',
                    'Host': 'www.jiqie.com',
                    'Origin': 'http://www.jiqie.com'
                }
        ids_0 = font2ids_dict[self.font_combobox.currentText()]
        ids_1 = color2ids_dict[self.color_combobox.currentText()]
        ids_2 = background2ids_dict[self.background_combobox.currentText()]
        data = {
                    'id': self.name_edit.text(),
                    'zhenbi': '20191123',
                    'id1': ids_0[0],
                    'id2': ids_0[1],
                    'id3': ids_1[0],
                    'id5': ids_2[1]
                }

        res = requests.post(url, headers=headers, data=data)
        image_url = re.findall(r'src="(.*?)"', res.text)[0]
        self.show_image_ext = image_url.split('.')[-1].split('?')[0]
        res = requests.get(image_url)
        fp = open('tmp.%s' % self.show_image_ext, 'wb')
        fp.write(res.content)
        fp.close()
        self.show_image = Image.open('tmp.%s' % self.show_image_ext).convert('RGB')
        self.updateimage()
        os.remove('tmp.%s' % self.show_image_ext)

        res = requests.post(url, headers=headers, data=data)
        image_url1 = re.findall(r'src="(.*?)"', res.text)[0]
        self.show_image_ext1 = image_url1.split('.')[-1].split('?')[0]
        res = requests.get(image_url1)
        fp = open('tmp.%s' % self.show_image_ext1, 'wb')
        fp.write(res.content)
        fp.close()
        self.show_image1 = Image.open('tmp.%s' % self.show_image_ext1).convert('RGB')
        self.updateimage()
        os.remove('tmp.%s' % self.show_image_ext1)

    '''更新界面上的图片'''
    def updateimage(self):
        if self.show_image is None:
            return
        fp = io.BytesIO()
        self.show_image.save(fp, 'JPEG')
        qtimage = QtGui.QImage()
        qtimage.loadFromData(fp.getvalue(), 'JPEG')
        qtimage_pixmap = QtGui.QPixmap.fromImage(qtimage)
        self.show_label.setPixmap(qtimage_pixmap)
        QtWidgets.QApplication.processEvents()

    '''保存签名'''
    def save(self):
        if self.show_image is None:
            return
        filename = QFileDialog.getSaveFileName(self, '保存', './sign.%s' % self.show_image_ext, '所有文件(*)')
        if filename[0]:
            self.show_image.save(filename[0])
            QDialog().show()

'''run'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ArtSignGenerator()
    gui.show()
    sys.exit(app.exec_())