from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import pytest

from spork_state import (
    Atom,
    VALIDATION_ERROR_MESSAGE,
    add_watch,
    atom,
    compare_and_set,
    deref,
    get_validator,
    is_atom,
    remove_watch,
    reset,
    reset_vals,
    set_validator,
    subscribe,
    swap,
    swap_vals,
)


def test_atom_and_functional_api() -> None:
    reference = atom(1)

    assert is_atom(reference)
    assert deref(reference) == 1
    assert reference.value == 1
    assert repr(reference) == "Atom(1)"
    assert reset(reference, 2) == 2
    assert reset_vals(reference, 3) == (2, 3)
    assert swap(reference, lambda value, amount: value + amount, 4) == 7
    assert swap_vals(reference, lambda value: value * 2) == (7, 14)
    assert Atom[int] is Atom


def test_update_failure_does_not_commit() -> None:
    reference = Atom(10)

    def fail(_value: int) -> int:
        raise RuntimeError("update failed")

    with pytest.raises(RuntimeError, match="update failed"):
        reference.swap(fail)

    assert reference.value == 10


def test_validator_runs_before_initialization_and_commit() -> None:
    non_negative = lambda value: value >= 0

    with pytest.raises(ValueError, match=VALIDATION_ERROR_MESSAGE):
        Atom(-1, validator=non_negative)

    reference = atom(1, non_negative)
    assert reference.validator is non_negative
    assert get_validator(reference) is non_negative

    with pytest.raises(ValueError, match=VALIDATION_ERROR_MESSAGE):
        reference.reset(-1)
    with pytest.raises(ValueError, match=VALIDATION_ERROR_MESSAGE):
        reference.swap(lambda _value: -1)

    assert reference.value == 1


def test_validator_can_only_be_replaced_when_it_accepts_current_value() -> None:
    original = lambda value: value > 0
    even = lambda value: value % 2 == 0
    reference = Atom(1, validator=original)

    with pytest.raises(ValueError, match=VALIDATION_ERROR_MESSAGE):
        set_validator(reference, even)

    assert reference.validator is original
    reference.reset(2)
    assert set_validator(reference, even) is reference
    assert reference.validator is even
    assert reference.set_validator(None) is reference
    assert reference.validator is None


def test_compare_and_set_uses_identity() -> None:
    expected = [1, 2]
    equal_but_distinct = [1, 2]
    replacement = [3]
    reference = Atom(expected)

    assert not compare_and_set(reference, equal_but_distinct, replacement)
    assert reference.value is expected
    assert reference.compare_and_set(expected, replacement)
    assert reference.value is replacement


def test_watches_observe_committed_state_and_can_be_removed() -> None:
    reference = Atom(1)
    events: list[tuple[object, int, int, int]] = []

    def watch(key: object, watched: Atom[int], old: int, new: int) -> None:
        events.append((key, watched.value, old, new))

    assert add_watch(reference, "audit", watch) is reference
    assert reference.reset(2) == 2
    assert events == [("audit", 2, 1, 2)]
    assert remove_watch(reference, "audit") is watch
    assert remove_watch(reference, "audit") is None
    reference.reset(3)
    assert len(events) == 1


def test_watches_execute_outside_the_atom_lock() -> None:
    reference = Atom(1)
    snapshots: list[int] = []

    def watch(_key: object, watched: Atom[int], _old: int, _new: int) -> None:
        reader = Thread(target=lambda: snapshots.append(watched.value))
        reader.start()
        reader.join(timeout=2)
        assert not reader.is_alive(), "watch callback ran while the atom lock was held"

    reference.add_watch("reader", watch)
    reference.reset(2)

    assert snapshots == [2]


def test_watch_failure_propagates_without_rolling_back() -> None:
    reference = Atom(1)

    def fail(*_args: object) -> None:
        raise RuntimeError("watch failed")

    reference.add_watch("failure", fail)

    with pytest.raises(RuntimeError, match="watch failed"):
        reference.reset(2)

    assert reference.value == 2


def test_identical_value_does_not_notify_but_equal_distinct_value_does() -> None:
    initial = [1]
    reference = Atom(initial)
    transitions: list[tuple[list[int], list[int]]] = []
    reference.add_watch(
        "changes",
        lambda _key, _ref, old, new: transitions.append((old, new)),
    )

    reference.reset(initial)
    assert transitions == []

    equal_but_distinct = [1]
    reference.reset(equal_but_distinct)
    assert transitions == [(initial, equal_but_distinct)]


def test_subscription_is_immediate_and_idempotently_unsubscribes() -> None:
    reference = Atom("ready")
    events: list[tuple[str, str]] = []

    unsubscribe = subscribe(
        reference,
        lambda old, new: events.append((old, new)),
        fire_immediately=True,
    )
    reference.reset("running")
    assert unsubscribe() is None
    assert unsubscribe() is None
    reference.reset("done")

    assert events == [("ready", "ready"), ("ready", "running")]


def test_swap_is_linearizable_across_threads() -> None:
    reference = Atom(0)
    workers = 8
    updates_per_worker = 2_000

    def increment_many() -> None:
        for _ in range(updates_per_worker):
            reference.swap(lambda value: value + 1)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(increment_many) for _ in range(workers)]
        for future in futures:
            future.result()

    assert reference.value == workers * updates_per_worker
