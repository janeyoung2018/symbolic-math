from random import random
class Node:
    operator = True
    operand = False
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
class Leaf:
    operator = False
    operand = True
    def __init__(self, data):
        self.data = data
def build(root):
    node = root
    if random() > 0.2:
        node.left = Leaf(2)
    else:
        node.left = build(Node('+'))
    if random() > 0.2:
        node.right = Leaf(3)
    else:
        node.right = build(Node('+'))
    return root
if __name__ == '__main__':
    random = build(Node('+'))
    root = Node('+')
    root.left = Leaf(2)
    root.right = Node('*')
    root.right.left = Leaf(3)
    root.right.right = Leaf(5)
    def traverse(root):
        print(root.data)
        if root.left.operator:
            traverse(root.left)
        else:
            print(root.left.data)
        if root.right.operator:
            traverse(root.right)
        else:
            print(root.right.data)
    traverse(root)