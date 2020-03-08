class Node(object):
    def __init__(self, path, children):
        self.children = children
        self.path = path

    def terminal_test(self):
        return False


class Leaf(Node):
    def __init__(self, path, value, children=None):
        super().__init__(path, children)
        if children is None:
            pass
        self.path = path
        self.value = value

    def terminal_test(self):
        return True


class Tree(object):
    def __init__(self):
        self.root = Node("Root", [
            Node("A", [
                Node("D", [
                    Leaf("M", 3),
                    Leaf("N", 10),
                    Leaf("O", 5)
                ]),
                Node("E", [
                    Leaf("P", 12),
                    Leaf("Q", 0),
                    Leaf("R", 4)
                ]),
                Node("F", [
                    Leaf("S", 6),
                    Leaf("T", 20),
                    Leaf("U", 8)
                ]),
            ]),
            Node("B", [
                Node("G", [
                    Leaf("V", 1),
                    Leaf("X", 2),
                    Leaf("Y", 6)
                ]),
                Node("H", [
                    Leaf("Z", 8),
                    Leaf("AA", 15),
                    Leaf("AB", 0)
                ]),
                Node("I", [
                    Leaf("AC", 5),
                    Leaf("AD", 2),
                    Leaf("AE", 3)
                ]),
            ]),
            Node("C", [
                Node("J", [
                    Leaf("AF", 10),
                    Leaf("AG", 20),
                    Leaf("AH", 7)
                ]),
                Node("K", [
                    Leaf("AI", 20),
                    Leaf("AJ", 30),
                    Leaf("AK", 40)
                ]),
                Node("L", [
                    Leaf("AL", 0),
                    Leaf("AM", 0),
                    Leaf("AN", 0)
                ]),
            ])
        ])

    def minimax_decision(self):

        def max_value(node):
            if node.terminal_test():
                return [node.value, node.path]
            val = -9999
            p = "none"
            for child in node.children:
                child_calc = min_value(child)
                if child_calc[0] > val:
                    val = child_calc[0]
                    p = child.path
            return [val, p]

        def min_value(node):
            if node.terminal_test():
                return [node.value, node.path]
            val = 9999
            p = "none"
            for child in node.children:
                child_calc = max_value(child)
                if child_calc[0] < val:
                    val = child_calc[0]
                    p = child.path
            return [val, p]

        [_, path] = max_value(self.root)
        return path


def main():
    tree = Tree()
    print('For the given tree, the minimax algorithm chooses move >> ' + tree.minimax_decision())


if __name__ == '__main__':
    main()
