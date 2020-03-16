start_range, end_range = 372 ** 2, 809 ** 2


def find_password(start, end):
    """
    params: start & end of range
    returns: list of possible passwords
    """
    final_container = list()
    # criteria I

    for i in range(start, end + 1):
        i = str(i)
        i = [x for x in i]
        container = list()
        for x in range(0, len(i)):
            if x == 0:
                container.append(i[x])
            else:
                try:
                    if i[x - 1] <= i[x]:
                        container.append(i[x])
                    else:
                        break
                except:
                    pass

        if len(container) == len(i):
            final_container.append(int(''.join(container)))

    print(f'{len(final_container)} after criteria I')

    # criteria II
    container = list()
    for i in final_container:
        i = str(i)
        i = [x for x in i]
        counter = {x: i.count(x) for x in i}

        if len(counter) > 1 and len(counter) < len(i) - 1:
            pairs = 0
            for _, v in counter.items():
                if v >= 2:
                    pairs += 1
                else:
                    continue

            if pairs >= 2:
                container.append("".join(i))

    print(f'{len(container)} after criteria II')

    return container


if __name__ == "__main__":
    func = find_password(start_range, end_range)
    print(f'Final answer: {len(func)}')
