import math
from abc import ABC
from dataclasses import dataclass
from enum import Enum

inp = open('day20.txt').read().strip()


class Signal(Enum):
    High = 0
    Low = 1


class Module(ABC):
    to: list['Module']

    def send(self, signal: Signal, frm: str):
        ...

    def receive(self) -> Signal | None:
        ...


@dataclass
class FlipFlop(Module):
    to: list[str]
    last: Signal = None
    powered: bool = False

    def send(self, signal: Signal, frm: str):
        self.last = signal
        if signal == Signal.Low:
            self.powered = not self.powered

    def receive(self):
        if self.last == Signal.Low:
            return Signal.High if self.powered else Signal.Low


@dataclass
class Broadcaster(Module):
    to: list[str]
    last: Signal = None

    def send(self, signal: Signal, frm: str):
        self.last = signal

    def receive(self):
        assert self.last is not None
        return self.last


@dataclass
class Conjunction(Module):
    to: list[str]
    lasts: dict[str, Signal] = None

    def send(self, signal: Signal, frm: str):
        if self.lasts is None:
            self.lasts = {}
        self.lasts[frm] = signal

    def receive(self):
        # print(self.lasts)
        return Signal.Low if all(sig is Signal.High for sig in self.lasts.values()) else Signal.High


modules = {}
for line in inp.split('\n'):
    mod, tos = line.split(' -> ')
    tos = tos.split(', ')
    if mod.startswith('%'):
        modules[mod[1:]] = FlipFlop(tos)
    elif mod.startswith('&'):
        modules[mod[1:]] = Conjunction(tos)
    elif mod == 'broadcaster':
        modules[mod] = Broadcaster(tos)
    else:
        print(mod)
        raise Exception()

for mod in modules:
    for to in modules[mod].to:
        if isinstance(modules.get(to, None), Conjunction):
            if modules[to].lasts is None:
                modules[to].lasts = {}
            modules[to].lasts[mod] = Signal.Low


def press_button(log=False):
    highs_sent = 0
    lows_sent = 1
    if log:
        print('button -low-> broadcaster')

    send_to = [('broadcaster', 'button', Signal.Low)]
    while send_to:
        to_send = []
        for mod, frm, signal in send_to:
            if mod not in modules:
                continue
            modules[mod].send(signal, frm)
            if (res := modules[mod].receive()):
                for to_mod in modules[mod].to:
                    if res is Signal.High:
                        highs_sent += 1
                    elif res is Signal.Low:
                        lows_sent += 1
                    if log:
                        print(f'{mod} -{"high" if res is Signal.High else "low"}-> {to_mod}')
                    to_send.append((to_mod, mod, res))
        send_to = to_send
    return highs_sent, lows_sent


# print(press_button())
#
# for _ in range(4):
#     press_button(True)
#     print()

highs = lows = 0
for _ in range(1000):
    nh, nl = press_button()
    highs += nh
    lows += nl
print(highs * lows)

modules = {}
for line in inp.split('\n'):
    mod, tos = line.split(' -> ')
    tos = tos.split(', ')
    if mod.startswith('%'):
        modules[mod[1:]] = FlipFlop(tos)
    elif mod.startswith('&'):
        modules[mod[1:]] = Conjunction(tos)
    elif mod == 'broadcaster':
        modules[mod] = Broadcaster(tos)
    else:
        print(mod)
        raise Exception()

for mod in modules:
    for to in modules[mod].to:
        if isinstance(modules.get(to, None), Conjunction):
            if modules[to].lasts is None:
                modules[to].lasts = {}
            modules[to].lasts[mod] = Signal.Low

froms = {key: None for key in modules['ft'].lasts}


def press_button(presses):
    worked = False
    send_to = [('broadcaster', 'button', Signal.Low)]
    while send_to:
        to_send = []
        for mod, frm, signal in send_to:
            if mod not in modules:
                continue
            modules[mod].send(signal, frm)
            if (res := modules[mod].receive()):
                for to_mod in modules[mod].to:
                    if to_mod == 'ft' and res is Signal.High and froms[mod] is None:
                        froms[mod] = presses
                    elif to_mod == 'ft' and res is Signal.High:
                        assert presses % froms[mod] == 0
                    to_send.append((to_mod, mod, res))
        send_to = to_send
    return worked


presses = 0
while any(val is None for val in froms.values()):
    presses += 1
    press_button(presses)
print(math.lcm(*froms.values()))
