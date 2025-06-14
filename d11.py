stones = open('testinput').read().strip().split(' ')
stones = open('input11').read().strip().split(' ')

class Node:
    def __init__(self, val=None, prev=None, next=None) -> None:
        self.val = val
        self.prev = prev
        self.next = next

    def __repr__(self) -> str:
        return f"Node({self.val})"

    def __iter__(self):
        current = self
        while current is not None:
            if current.val is None:
                break
            yield current
            current = current.next

start = Node()
end = Node()
start.next = end
end.prev = start

def insert_after(node: Node, to_be_inserted: Node) -> None:
    to_be_inserted.next = node.next
    to_be_inserted.prev = node
    node.next = to_be_inserted

def split_node(old_node: Node, new_left: Node, new_right: Node) -> None:
    new_left.prev = old_node.prev
    old_node.prev.next = new_left
    new_left.next = new_right
    new_right.prev = new_left
    new_right.next = old_node.next
    old_node.next.prev = new_right

# initialize the list with input
current = start
for s in stones:
    n = Node(int(s))
    insert_after(current, n)
    current = n

# run transformations for every 'blink'
i = 25
for ii in range(i):
    n = start.next
    #print('START ', n)
    while n:
        if n is None or n.val is None:
            break
        # #print(f'transforming node{n}')
        if n.val == 0:
            n.val = 1
            n = n.next
        # split into two halfs
        elif len(str(n)) % 2 == 0:
            #print('splitting into two halfs num ' , str(n))
            num = str(n.val)
            mid = len(num) // 2
            left = num[:mid]
            if len(left) > 1:
                left = left.lstrip('0')
            if left == '':
                left = 0
            #print('left ', left)
            right = num[mid:]
            if len(right) > 1:
                right = right.lstrip('0')
            if right == '':
                right = 0
            #print('right ', right)
            left_node = Node(int(left))
            right_node = Node(int(right))
            split_node(n, left_node, right_node)
            n = right_node.next
        else:
            # #print('multiply by 2024 ', n)
            n.val = n.val * 2024
            n = n.next

sol = []
for n in start.next:
    sol.append(str(n.val))
print('='*100)
# print(' '.join(sol))
print(len(sol))
