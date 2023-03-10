import img2pdf
import os

# 列出文件夹里面的所有文件名和路径
filepath = os.getcwd() + '\data'
files = os.listdir(filepath)
print(files)
# 排序，防止合并后文件页面乱序
filedict = {int(i.split('.')[0].split('_')[1]): i for i in files}
print(filedict)
files = [filedict[i] for i in sorted(filedict)]
# # 文件名+路径
files = ['./data/' + i for i in files]
print(files)
# # 把所有图片拼接为pdf
with open('./testpdf1.pdf', mode='wb') as f:
    f.write(img2pdf.convert(files))

