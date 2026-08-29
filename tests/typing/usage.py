from spork_state import Atom, atom, compare_and_set, deref, reset, swap

counter: Atom[int] = atom(0, lambda value: value >= 0)
value: int = counter.swap(lambda current, amount: current + amount, 2)
assert value == 2
assert swap(counter, lambda current: current + 1) == 3
assert reset(counter, 4) == 4
assert deref(counter) == 4
assert compare_and_set(counter, counter.value, 5)

transitions: list[tuple[int, int]] = []
unsubscribe = counter.subscribe(lambda old, new: transitions.append((old, new)))
unsubscribe()
