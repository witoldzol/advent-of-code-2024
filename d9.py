f = open('testinput')
f = open('input9')
input = f.read().strip()
FILES = {}
EMPTY_SECTORS = []
def generate_blocks(input:str) -> list[str]:
    input_list = list(input)
    blocks = []
    file_index = 0
    current_idx = 0
    for i in range(len(input_list)):
        if i % 2 == 0:
            file_size = int(input_list[i])
            FILES[str(file_index)] = (current_idx, file_size)
            for _ in range(file_size):
                blocks.append(str(file_index))
            file_index += 1
            current_idx += file_size
        else:
            empty_block_size = int(input_list[i])
            for _ in range(empty_block_size):
                blocks.append('.')
            EMPTY_SECTORS.append((current_idx, empty_block_size))
            current_idx += empty_block_size
    return blocks

def compact_entire_files(blocks) -> None:
    for file, file_info in reversed(FILES.items()):
        # print(f'processing file {file}')
        file_idx, file_size = file_info
        for sector_index, sector_info  in enumerate(EMPTY_SECTORS):
            if sector_info is None:
                continue
            empty_idx, empty_size = sector_info
            # if we can fit the file
            if file_size <= empty_size:
                # print(f'found block to fits {file}, block idx {empty_idx}, size {empty_size}')
                file = blocks[file_idx]
                # move file to empty sector
                for i in range(empty_idx, empty_idx + file_size):
                    blocks[i] = file
                # remove file from previous location
                for i in range(file_idx, file_idx + file_size):
                    blocks[i] = '.'
                # update empty sector
                if file_size == empty_size:
                    EMPTY_SECTORS[sector_index] = None
                else:
                    new_start_idx = empty_idx + file_size
                    new_size = empty_size - file_size
                    EMPTY_SECTORS[sector_index] = (new_start_idx, new_size)
                break
            # else:
            #     print(f'did not find empty block for file {file}')


def gen_checksum(blocks: list[str]) -> int:
    checksum = 0
    for i,x in enumerate(blocks):
        if x == '.':
            continue
        checksum += i * int(x)
    return checksum

blocks = generate_blocks(input)
expected = '00...111...2...333.44.5555.6666.777.888899'
# assert expected == ''.join(blocks)

# print(FILES)
compact_entire_files(blocks)
# assert '00992111777.44.333....5555.6666.....8888..' == ''.join(blocks), ''.join(blocks)

print('checksum')
print(gen_checksum(blocks))
# 8444425634594 = too high
