from graphviz import Digraph

class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = BSTNode(key)
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key)
            else:
                self._insert(node.left, key)
        else:
            if node.right is None:
                node.right = BSTNode(key)
            else:
                self._insert(node.right, key)

    def visualize(self, filename='bst'):
        dot = Digraph()
        self._visualize(dot, self.root)
        dot.render(filename, format='png', cleanup=True)

    def _visualize(self, dot, node):
        if node:
            dot.node(str(node.key))
            if node.left:
                dot.edge(str(node.key), str(node.left.key))
                self._visualize(dot, node.left)
            if node.right:
                dot.edge(str(node.key), str(node.right.key))
                self._visualize(dot, node.right)

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def visualize(self, filename='avl'):
        dot = Digraph()
        self._visualize(dot, self.root)
        dot.render(filename, format='png', cleanup=True)

    def _visualize(self, dot, node):
        if node:
            dot.node(str(node.key))
            if node.left:
                dot.edge(str(node.key), str(node.left.key))
                self._visualize(dot, node.left)
            if node.right:
                dot.edge(str(node.key), str(node.right.key))
                self._visualize(dot, node.right)

class RBNode:
    def __init__(self, key, color='red'):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.TNULL = RBNode(0, 'black')
        self.root = self.TNULL

    def insert(self, key):
        node = RBNode(key)
        node.left = self.TNULL
        node.right = self.TNULL
        node.parent = None

        if self.root == self.TNULL:
            node.color = 'black'
            self.root = node
        else:
            self._insert(self.root, node)
            self._fix_insert(node)

    def _insert(self, root, node):
        if root != self.TNULL:
            if node.key < root.key:
                if root.left == self.TNULL:
                    root.left = node
                    node.parent = root
                else:
                    self._insert(root.left, node)
            else:
                if root.right == self.TNULL:
                    root.right = node
                    node.parent = root
                else:
                    self._insert(root.right, node)
        else:
            root = node

    def _fix_insert(self, k):
        while k != self.root and k.parent.color == 'red':
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == 'red':
                    u.color = 'black'
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self._left_rotate(k)
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self._right_rotate(k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == 'red':
                    u.color = 'black'
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self._right_rotate(k)
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self._left_rotate(k.parent.parent)
        self.root.color = 'black'

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def visualize(self, filename='rbt'):
        dot = Digraph()
        self._visualize(dot, self.root)
        dot.render(filename, format='png', cleanup=True)

    def _visualize(self, dot, node):
        if node != self.TNULL:
            dot.node(str(node.key), color=node.color)
            if node.left != self.TNULL:
                dot.edge(str(node.key), str(node.left.key))
                self._visualize(dot, node.left)
            if node.right != self.TNULL:
                dot.edge(str(node.key), str(node.right.key))
                self._visualize(dot, node.right)

# 示例
keys = [35, 51, 30, 63, 72, 15, 8, 58, 46, 24]

bst = BST()
for key in keys:
    bst.insert(key)
bst.visualize('bst')

avl = AVL()
for key in keys:
    avl.insert(key)
avl.visualize('avl')

rbt = RedBlackTree()
for key in keys:
    rbt.insert(key)
rbt.visualize('rbt')
# 不要功能2

#功能3
