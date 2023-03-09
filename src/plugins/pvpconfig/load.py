import os


def load_config(name):
    arr = ""
    isIn = False
    for root, dirs, _ in os.walk('src/plugins/pvpconfig/config'):
        if name in dirs:
            isIn = True
            arr = "以下是" + name + "在Pokemmo PVP中的常见配置: "
            path = os.path.join(root, name)
            for _, _, files in os.walk(path):
                for file in files:
                    with open(os.path.join(path, file), 'r') as f:
                        content = f.read()
                        arr = arr + "\n---------\n" + content
    
    if not isIn:
        arr = "暂无" + name + "的相关配置QAQ"
    return arr

