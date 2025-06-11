f = open('testinput')
f = open('input9')
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

blocks = generate_blocks(input)
# expected = '00...111...2...333.44.5555.6666.777.888899'
# assert expected == ''.join(blocks)

def compact(blocks: list[str]) -> list[str]:
    empty_sectors = [i for i,x in enumerate(blocks) if x == '.']
    empty_sector_index = 0
    for counter,i in enumerate(range(len(blocks)-1,-1, -1)):
        if counter >= len(empty_sectors):
            break
        if blocks[i] != '.':
            blocks[empty_sectors[empty_sector_index]] = blocks[i]
            empty_sector_index += 1
            blocks[i] = '.'

compact(blocks)
# assert '0099811188827773336446555566..............' == ''.join(blocks)

def gen_checksum(blocks: list[str]) -> int:
    checksum = 0
    for i,x in enumerate(blocks):
        if x == '.':
            break
        checksum += i * int(x)
    return checksum
print('checksum')
print(gen_checksum(blocks))
