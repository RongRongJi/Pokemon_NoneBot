import os


def load_config(name):
    arr = ""
    isIn = False
    for root, dirs, files in os.walk('src/plugins/pvpconfig/pokemon'):

        if name in files:
            isIn = True
            arr = "以下是" + name + "在Pokemmo PVP中的常见配置: "
            file = os.path.join(root, name)
            with open(file, 'r') as f:
                content = f.read()
                arr = arr + "\n---------\n" + content
    
    if not isIn:
        arr = "暂无" + name + "的相关配置QAQ"
    return arr

