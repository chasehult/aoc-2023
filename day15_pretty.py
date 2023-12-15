import sys
from collections.abc import Hashable, Iterable, MutableMapping
from dataclasses import dataclass

type LinkedList = 'Node'


class Node[T](Iterable[T]):
    def __init__(self, value: T):
        self.value = value
        self.next: Node[T] | None = None

    def __iter__(self):
        cur = self
        while cur is not None:
            yield cur.value
            cur = cur.next

    def __repr__(self):
        return f'Node<{self.value} -> {self.next}>'


@dataclass
class Pair[K, V]:
    key: K
    value: V


class HashMap[K: Hashable, V](MutableMapping[K, V]):
    def __init__(self, size: int):
        self.size = size
        self._internal_dict: dict[int, LinkedList[Pair[K, V]]] = {}

    def __getitem__(self, key: K):
        hashed = (hash(key) % self.size) + 1
        for pair in self._internal_dict.get(hashed, []):
            if key == pair.key:
                return pair.value
        raise KeyError(f"Key {key!r} not found.")

    def __setitem__(self, key: K, value: V):
        hashed = (hash(key) % self.size) + 1
        if hashed not in self._internal_dict:
            self._internal_dict[hashed] = Node(Pair(key, value))
        else:
            cur = self._internal_dict[hashed]
            while cur.next is not None:
                if cur.value.key == key:
                    cur.value.value = value
                    return
                cur = cur.next
            else:
                if cur.value.key == key:
                    cur.value.value = value
                else:
                    cur.next = Node(Pair(key, value))

    def __delitem__(self, key: K):
        hashed = (hash(key) % self.size) + 1
        if hashed not in self._internal_dict:
            return
        if self._internal_dict[hashed].value.key == key:
            self._internal_dict[hashed] = self._internal_dict[hashed].next
            if self._internal_dict[hashed] is None:
                del self._internal_dict[hashed]
            return
        cur = self._internal_dict[hashed]
        while cur.next is not None and cur.next.value.key != key:
            cur = cur.next
        if cur.next is None:
            return
        cur.next = cur.next.next

    def __iter__(self):
        for ll in self._internal_dict.values():
            for pair in ll:
                yield pair.key

    def __len__(self):
        return sum(1 for _ in self)

    def __str__(self):
        return str(self._internal_dict)


########################################################################


class Lens:
    def __init__(self, label: str):
        self.label = label

    def __hash__(self):
        value = 0
        for char in self.label:
            value = (value + ord(char)) * 17 % 256
        return value

    def __eq__(self, other):
        return isinstance(other, Lens) and self.label == other.label

    def __repr__(self):
        return f"Lens<{self.label}>"


class HolidayASCIIStringHelperManualArrangementProcedure(HashMap):
    def focusing_power(self):
        total = 0
        for box_no, ll in self._internal_dict.items():
            for box_idx, pair in enumerate(ll, 1):
                total += box_no * box_idx * pair.value
        return total


def main():
    if len(sys.argv) == 1:
        file_name = 'day15.txt'
    else:
        file_name = sys.argv[1]
    with open(file_name) as f:
        instructions = f.read().strip().split(',')

    total = 0
    for inst in instructions:
        total += hash(Lens(inst))
    print(f"Part 1: {total}")

    hashmap = HolidayASCIIStringHelperManualArrangementProcedure(256)
    for inst in instructions:
        if '=' in inst:
            label, value = inst.split('=')
            lens, value = Lens(label), int(value)
            hashmap[lens] = value
        elif '-' in inst:
            lens = Lens(inst.rstrip('-'))
            del hashmap[lens]
    print(f"Part 2: {hashmap.focusing_power()}")


if __name__ == '__main__':
    main()
