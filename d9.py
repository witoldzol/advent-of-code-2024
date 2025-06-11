f = open('testinput')
input = f.read().strip()
print(input)

def generate_blocks(input:str) -> list[str]:
    input_list = list(input)
    blocks = []
    file_index = 0
    for i in range(len(input_list)):
        if i % 2 == 0:
            file_size = int(input_list[i])
            for _ in range(file_size):
                blocks.append(str(file_index))
            file_index += 1
        else:
            empty_block_size = int(input_list[i])
            for _ in range(empty_block_size):
                blocks.append('.')
    return blocks

expected = '00...111...2...333.44.5555.6666.777.888899'
assert expected == ''.join(generate_blocks(input))
