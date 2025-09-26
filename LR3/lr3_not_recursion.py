def gen_bin_tree(height:int , root:int):
    def left_leaf(root):
        return (root - 8) * 3

    def right_leaf(root):
        return (root + 8) * 2
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
