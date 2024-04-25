import re

def check_macor_match(file_path):
    content = ''
    with open(file_path, "r") as f:
        content = f.read()
    p = re.compile(r'#define\s*(\w+_\w+_SEC_\w+)')
    # for result in p.finditer(content):
    #     print(result.groupdict())
    res = p.findall(content)

    if len(res) % 2 != 0:
        return False

    while len(res):
        a = res.pop()
        b = res.pop()
        if a.replace("STOP", "START") != b:
            return False
        # print(f"{a:<50} <==> {b:<50}")

    return True

if __name__ == "__main__":
    print(check_macor_match("test.c"))
    pass