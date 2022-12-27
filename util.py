import os


#폴더 생성 함수
#폴더가 이미 있으면 만들지않고 없으면 만든다.
def createFolder(directory):
    try:
        # 폴더가 없는가?
        if not os.path.exists(directory):
            os.mkdir(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

def isEmpty(list):
   for element in list:
     if element:
       return True
     return False


def pretty_print(current, parent=None, index=-1, depth=0):
    for i, node in enumerate(current):
        pretty_print(node, current, i, depth + 1)
    if parent is not None:
        if index == 0:
            parent.text = '\n' + ('\t' * depth)
        else:
            parent[index - 1].tail = '\n' + ('\t' * depth)
        if index == len(parent) - 1:
            current.tail = '\n' + ('\t' * (depth - 1))
