import os
import glob

text_heeader = '''---
title: {title}
date: 2022/7/13 20:46:25
---
'''

path = "C:/Users/Administrator/Desktop/blogfile"

if __name__ == "__main__":
    for dirpath, dirnames, filenames in os.walk(path):
        for filepath in filenames:
            item = os.path.join(dirpath, filepath)
            if ".md" in item:
                md = open(item, 'r+', encoding='utf-8')
                context = md.read()
                md.seek(0)
                md.write(text_heeader.format(title = filepath[0:-3]) + context)

    # print(text_heeader)
    # with open("item.txt", 'r+', encoding='utf-8') as txt:
    #     # print(txt.write("item.txt\n"))
    #     # print(txt.write("encoding.txt\n"))
    #     # print(txt.write("txt.txt\n"))
    #     str1 = txt.read()
    #     txt.seek(0)
    #     txt.write(text_heeader+str1)
    #     # print(str1)
