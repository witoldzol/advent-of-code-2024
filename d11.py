stones = open('testinput').read().strip().split(' ')

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

# initialize the list with input
current = start
for s in stones:
    n = Node(int(s))
    insert_after(current, n)
    current = n

# run transformations for every 'blink'
# for n in start.next:
n = start.next
while n:
    print(f'transforming node {n}')
    if n.val == 0:
        n.val = 1
    elif len(str(n)) % 2 == 0:
        num = str(n.val)
        mid = len(num) // 2
        left = num[:mid]
        if len(left) > 1:
            left = left.rstrip('0')
        right = num[mid:]
        if len(right) > 1:
            right = right.rstrip('0')
        # print(f'SPLITTING {num}')
        # print('left')
        # print(left)
        # print('right')
        # print(right)
        left_node = Node(int(left))
        right_node = Node(int(right))
        insert_after(n, left_node)
        insert_after(left_node, right_node)
        n = right_node.next
    else:
        n.val = n.val * 2024

for n in start.next:
    print(n)
