def left_leaf(root):
    return (root - 8) * 3

def right_leaf(root):
    return (root + 8) * 2

def gen_bin_tree(height:int , root:int) -> list:
    if height == 0:
        return [root]
    else:
        return [root] + gen_bin_tree(height - 1 , left_leaf(root)) +  gen_bin_tree(height - 1, right_leaf(root))
print(gen_bin_tree(2,18))
