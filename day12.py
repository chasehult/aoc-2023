from functools import cache

inp = open('day12.txt').read().strip()


def works(row, cnts):
    cnts = cnts[:]
    cnt = 0
    try:
        for c in row:
            if c == '#':
                cnt += 1
            elif c == '.':
                if cnt == 0:
                    continue
                if cnt != cnts.pop(0):
                    return False
                cnt = 0
        if cnt == 0:
            return not len(cnts)
        return cnt == cnts.pop(0) and len(cnts) == 0
    except IndexError:
        return False


def iterate_over(row):
    q_cnt = row.count('?')
    for x in range(2 ** q_cnt):
        bin_x = bin(x)[2:].zfill(q_cnt)
        news = ''
        cnt = 0
        for c in row:
            if c != '?':
                news += c
            elif bin_x[cnt] == '1':
                news += '.'
                cnt += 1
            else:
                news += '#'
                cnt += 1
        yield news


# total = 0
# for row in inp.split('\n'):
#     sprs, cnts = row.split()
#     cnts = [int(c) for c in cnts.split(',')]
#     for repl in iterate_over(sprs):
#         if works(repl, cnts):
#             total += 1
# print(total)

# total = 0
# for row in inp.split('\n'):
#     sprs, cnts = row.split()
#     cnts = [int(c) for c in cnts.split(',')]
#     sprs = '?'.join([sprs for _ in range(5)])
#     cnts = cnts * 5
#     for repl in iterate_over(sprs):
#         if works(repl, cnts):
#             total += 1
# print(total)

# @cache
# def get_solution(sprs, cnts, lvl = 0):
#     print(f"{'  ' * lvl}| {str(sprs)} {cnts}")
#     if sprs == '' and cnts == ():
#         print(f"{'  ' * lvl}| V")
#         return 1
#     elif sprs == '':
#         print(f"{'  ' * lvl}| X")
#         return 0
#     elif cnts == () and sprs[0] == '#':
#         print(f"{'  ' * lvl}| X")
#         return 0
#     elif cnts == ():
#         return get_solution(sprs[1:], (), lvl)
#
#     if cnts[0] == 0:
#         print(f"{'  ' * lvl}| X")
#         return 0
#
#     if len(sprs) == 1:
#         match sprs[0]:
#             case '#':
#                 print(f"{'  ' * lvl}| {'V' if cnts == (1,) else 'X'}")
#                 return cnts == (1,)
#             case '?':
#                 print(f"{'  ' * lvl}| {'V' if cnts in ((1,), ()) else 'X'}")
#                 return cnts in ((1,), ())
#             case '.':
#                 print(f"{'  ' * lvl}| {'V' if cnts == () else 'X'}")
#                 return cnts == ()
#
#     match sprs[0]:
#         case '#':
#             # match sprs[1]:
#             #     case '.':
#             #         if cnts[0] == 1:
#             #             return get_solution(sprs[2:], cnts[1:], lvl)
#             #         else:
#             #             print(f"{'  ' * lvl}| X")
#             #             return 0
#             #     case '#':
#             #         new_cnts = tuple([cnts[0]-1, *cnts[1:]])
#             #         return get_solution(sprs[1:], new_cnts, lvl)
#             #     case '?':
#             #         if cnts[0] == 2:
#             #             if len(sprs) == 2:
#             #                 print(f"{'  ' * lvl}| V")
#             #                 return 1
#             #             elif sprs[2] in ('.', '?'):
#             #                 return get_solution(sprs[3:], cnts[1:], lvl)
#             #             else:
#             #                 print(f"{'  ' * lvl}| X")
#             #                 return 0
#             #         elif cnts[0] == 1:
#             #             return get_solution(sprs[2:], cnts[1:], lvl)
#             #         else:
#             #             new_cnts = tuple([cnts[0] - 2, *cnts[1:]])
#             #             return get_solution(sprs[2:], new_cnts, lvl)
#             numhashes = len(re.match(r'#+', sprs).group())
#             if numhashes > cnts[0]:
#                 print(f"{'  ' * lvl}| X")
#                 return 0
#             elif numhashes == cnts[0]:
#                 return get_solution(sprs[numhashes:], cnts[1:], lvl)
#             else:
#                 new_cnts = tuple([cnts[0] - 1, *cnts[1:]])
#                 return get_solution(sprs[numhashes:], new_cnts, lvl)
#         case '.':
#             return get_solution(sprs[1:], cnts, lvl)
#         case '?':
#             match sprs[1]:
#                 case '.':
#                     if cnts[0] == 1:
#                         return get_solution(sprs[2:], cnts[1:], lvl)
#                     else:
#                         print(f"{'  ' * lvl}| X")
#                         return 0
#                 case '#':
#                     if cnts[0] == 1:
#                         return get_solution(sprs[1:], cnts, lvl)
#                     else:
#                         new_cnts = tuple([cnts[0] - 1, *cnts[1:]])
#                         s1 = get_solution(sprs[1:], cnts, lvl + 1)
#                         print(f"{'  ' * (lvl+1)}| ---")
#                         s2 = get_solution(sprs[1:], new_cnts, lvl + 1)
#                         return s1 + s2
#                 case '?':
#                     if cnts[0] == 1:
#                         s1 = get_solution(sprs[2:], cnts[1:], lvl + 1)
#                         print(f"{'  ' * (lvl+1)}| ---")
#                         s2 = get_solution(sprs[1:], cnts, lvl + 1)
#                         print(f"{'  ' * (lvl+1)}| ---")
#                         s3 = get_solution(sprs[2:], cnts, lvl + 1)
#                         return s1 + s2 + s3
#                     else:
#                         new_cnts = tuple([cnts[0] - 1, *cnts[1:]])
#                         s1 = get_solution(sprs[1:], cnts, lvl + 1)
#                         print(f"{'  ' * (lvl+1)}| ---")
#                         s2 = get_solution(sprs[1:], new_cnts, lvl + 1)
#                         print(f"{'  ' * (lvl+1)}| ---")
#                         s3 = get_solution(sprs[2:], new_cnts, lvl + 1)
#                         return s1 + s2 + s3

"""
def debug_handler(*, cache):
    def decorator(f):
        seen = {}

        @wraps(f)
        def newf(sprs: str, cnts: tuple, *, inmatch: bool = False,
                 lvl: int = 0, is_split: bool = False):
            if cache and (sprs, cnts, inmatch) in seen:
                return seen[(sprs, cnts, inmatch)]
            if is_split:
                print(f"{'  ' * lvl}| ---")
            print(f"{'  ' * lvl}| {str(sprs)} {cnts} {'<>' if inmatch else ''}")
            res = f(sprs, cnts, inmatch, lvl, is_split)
            if res is True:
                print(f"{'  ' * lvl}| V")
            elif res is False:
                print(f"{'  ' * lvl}| X")
            seen[(sprs, cnts, inmatch)] = res
            return int(res)

        return newf

    return decorator


@debug_handler(cache=False)
def get_solution(sprs: str, cnts: tuple, inmatch: bool = False,
                 lvl: int = 0, is_split: bool = False):
    if sprs == '' and cnts == ():
        return True
    elif sprs == '':
        return False
    elif cnts == () and sprs[0] == '#':
        return False
    elif cnts == ():
        return get_solution(sprs[1:], cnts, lvl=lvl)

    if cnts[0] == 0:
        print(f"{'  ' * lvl}| X")
        return False

    if len(sprs) == 1:
        match sprs[0]:
            case '#':
                return cnts == (1,)
            case '?':
                return cnts in ((1,), ())
            case '.':
                return cnts == ()

    match sprs[0]:
        case '.':
            if inmatch:
                return False
            return get_solution(sprs[1:], cnts, lvl=lvl)
        case '#':
            numhashes = len(re.match(r'#+', sprs).group())
            if numhashes > cnts[0]:
                return 0
            elif numhashes == cnts[0]:
                return get_solution(sprs[numhashes:], cnts[1:], lvl=lvl)
            else:
                new_cnts = tuple([cnts[0] - numhashes, *cnts[1:]])
                return get_solution(sprs[numhashes:], new_cnts, inmatch=True, lvl=lvl)
        case '?':
            if cnts[0] == 1 and inmatch:
                match sprs[1]:
                    case '#':
                        return False
                    case '.' | '?':
                        return get_solution(sprs[2:], cnts[1:], lvl=lvl)
            if inmatch:
                new_cnts = tuple([cnts[0] - 1, *cnts[1:]])
                return get_solution(sprs[1:], new_cnts, inmatch=True, lvl=lvl)
            elif cnts[0] == 1:
                match sprs[1]:
                    case '#':
                        return get_solution(sprs[1:], cnts, lvl=lvl)
                    case '.':
                        return get_solution(sprs[1:], cnts[1:], lvl=lvl + 1, is_split=True) \
                            + get_solution(sprs[1:], cnts, lvl=lvl + 1, is_split=True)
                    case '?':
                        if len(sprs) == 2:
                            return get_solution(sprs[1:], cnts[1:], inmatch=True, lvl=lvl + 1, is_split=True) \
                                + get_solution(sprs[1:], cnts[1:], lvl=lvl + 1, is_split=True)
                        match sprs[2]:
                            case '#':
                                return get_solution(sprs[2:], cnts, lvl=lvl + 1, is_split=True) \
                                    + get_solution(sprs[2:], cnts[1:], lvl=lvl + 1, is_split=True)
                            case '.':
                                return get_solution(sprs[2:], cnts, lvl=lvl + 1, is_split=True) \
                                    + get_solution(sprs[2:], cnts[1:], lvl=lvl + 1, is_split=True) \
                                    + get_solution(sprs[2:], cnts[1:], lvl=lvl + 1, is_split=True)
                            case '?':
                                return get_solution(sprs[2:], cnts, lvl=lvl + 1, is_split=True) \
                                    + get_solution(sprs[2:], cnts[1:], lvl=lvl + 1, is_split=True) \
                                    + get_solution(sprs[2:], cnts, lvl=lvl + 1, is_split=True)
            match sprs[1]:
                case '#':
                    new_cnts = tuple([cnts[0] - 1, *cnts[1:]])
                    return get_solution(sprs[1:], cnts, lvl=lvl + 1, is_split=True) \
                        + get_solution(sprs[1:], new_cnts, lvl=lvl + 1, is_split=True)
                case '.':
                    return get_solution(sprs[2:], cnts, lvl=lvl)
                case '?':
                    if len(sprs) == 2:
                        if cnts == (2,):
                            return True
                        return False
                    new_cnts = tuple([cnts[0] - 1, *cnts[1:]])
                    return get_solution(sprs[1:], cnts, lvl=lvl + 1, is_split=True) \
                        + get_solution(sprs[1:], new_cnts, inmatch=True, lvl=lvl + 1, is_split=True)
"""

@cache
def get_solution(sprs, cnts):
    # print(sprs, cnts)
    if sprs == '' and cnts == ():
        return True
    elif sprs == '':
        return False
    elif cnts == () and sprs[0] == '#':
        return False
    elif cnts == ():
        return get_solution(sprs[1:], cnts)
    elif cnts[0] == 0:
        return False
    elif cnts[0] > len(sprs):
        return False
    elif cnts[0] == len(sprs):
        if len(cnts) > 1:
            return False
        return all(c in ('#', '?') for c in sprs)

    if len(sprs) == 1:
        match sprs[0]:
            case '#':
                return cnts == (1,)
            case '?':
                return cnts in ((1,), ())
            case '.':
                return cnts == ()

    match sprs[0]:
        case '#':
            if all(c in ('#', '?') for c in sprs[:cnts[0]]) \
                    and sprs[cnts[0]] in ('.', '?'):
                return get_solution(sprs[cnts[0] + 1:], cnts[1:])
            return 0
        case '.':
            return get_solution(sprs[1:], cnts)
        case '?':
            if all(c in ('#', '?') for c in sprs[:cnts[0]]) \
                    and sprs[cnts[0]] in ('.', '?'):
                return get_solution(sprs[1:], cnts) \
                    + get_solution(sprs[cnts[0] + 1:], cnts[1:])
            return get_solution(sprs[1:], cnts)


total = 0
for row in inp.split('\n'):
    sprs, cnts = row.split()
    cnts = [int(c) for c in cnts.split(',')]
    sol = get_solution(sprs, tuple(cnts))
    # print(sprs, sol)
    total += sol
print(total)

total = 0
for row in inp.split('\n'):
    sprs, cnts = row.split()
    cnts = [int(c) for c in cnts.split(',')]
    sol = get_solution('?'.join(sprs for _ in range(5)), tuple(cnts) * 5)
    # print(sprs, sol)
    total += sol
print(total)
