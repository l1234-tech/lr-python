def cnt_brenches(height):
    cnt = 0
    for i in range(0 , height + 1):
        cnt += 2 ** i
    return cnt

def left_leaf(root):
    return (root - 8) * 3

def right_leaf(root):
    return (root + 8) * 2

def gen_bin_tree(height:int , root:int):
    tree = []
    tree.append(root)
    cnt = 0
    if height == 0:
        return tree
    if height > 0:
        while cnt < height:
            cnt += 1
            flag = 2 ** (cnt - 1)
            for i in tree[-flag:]:
                tree.append(left_leaf(i))
                tree.append(right_leaf(i))
        return tree
print(gen_bin_tree(5 , 18))
