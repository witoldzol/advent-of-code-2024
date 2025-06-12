from collections import deque

f = open('input9')
input = f.read().strip()
# spaces and files
files = deque()
spaces = []
index = 0
for i, c in enumerate(input):
    size = int(c)
    if i % 2 == 0:
        file_name = i // 2
        files.append((size, index, file_name))
    else:
        spaces.append((size, index, '.'))
    index += size
checksum = 0
# move files to empty spaces
while files:
    f_size, f_index, file_name = files.pop()
    moved = False
    for s_i, s in enumerate(spaces):
        if s is None:
            continue
        s_size, s_index, _ = s
        # don't move files to the 'right', only 'left'
        if s_index >= f_index:
            break
        if f_size <= s_size:
            # calc the checksum at new position
            for ii in range(s_index, s_index + f_size):
                checksum += ii * file_name
            # update the free space
            new_s_size = s_size - f_size
            new_s_index = s_index + f_size
            if new_s_size == 0:
                spaces[s_i] = None
            else:
                spaces[s_i] = (new_s_size, new_s_index, '.')
            # stop looking for a space
            moved = True
            break
    if not moved:
        # we couldn't find big enough space, but we still need to calculate the checksum
        for ii in range(f_index, f_index + f_size):
            checksum += ii * file_name
print(checksum)
