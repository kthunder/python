import os

src = "C:\\GIT\\GIT-ChangSha\\a8v2_mcal-safetylib-bsp\\m7\\assembly\\plugins\\"
dest = "C:\\IDE\\EB\\tresos\\plugins\\"

if __name__ == "__main__":
    for dir_item in os.listdir(src):
        print(src + dir_item)
        os.symlink(src + dir_item, dest + dir_item)
