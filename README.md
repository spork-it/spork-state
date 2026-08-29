# spork-state

[![Tests](https://github.com/spork-it/spork-state/actions/workflows/test.yml/badge.svg)](https://github.com/spork-it/spork-state/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/spork-state.svg)](https://pypi.org/project/spork-state/)
[![Python](https://img.shields.io/pypi/pyversions/spork-state.svg)](https://pypi.org/project/spork-state/)

Thread-safe state management with one implementation for both [Spork](https://github.com/spork-it/spork-lang) and Python.

`spork-state` provides `Atom`: a mutable reference whose updates are synchronized, validated before commit, and observable through synchronous watches. The implementation and type declarations live in Spork; `spork build` generates idiomatic package-level Spork and typed Python APIs directly from the manifest.

## Install

Python projects:

```bash
python -m pip install spork-state
```

Spork projects add the package to `spork.it` and synchronize the project environment:

```clojure
:dependencies ["spork-state>=0.2,<0.3"]
```

```bash
spork sync
```

`spork-state` supports Python 3.10–3.14, including free-threaded 3.14.

## Python API

```python
from spork_state import Atom

counter = Atom(0, validator=lambda value: value >= 0)

unsubscribe = counter.subscribe(
    lambda old, new: print(f"{old} -> {new}"),
    fire_immediately=True,
)

counter.swap(lambda value, amount: value + amount, 3)
assert counter.value == 3
assert counter.compare_and_set(counter.value, 4)

unsubscribe()
```

Functional equivalents (`atom`, `deref`, `swap`, `reset`, and others) are also exported.

## Spork API

```clojure
(ns example.counter
  (:require [spork-state :as state]))

(def counter (state.atom 0 (fn [value] (>= value 0))))

(state.add-watch! counter :log
  (fn [key reference old-value new-value]
    (print old-value "->" new-value)))

(state.swap! counter (fn [value amount] (+ value amount)) 3)
(assert (= (state.deref counter) 3))
```

The core Spork functions are `atom`, `atom?`, `deref`, `swap!`, `swap-vals!`, `reset!`, `reset-vals!`, `compare-and-set!`, `add-watch!`, `remove-watch!`, `get-validator`, and `set-validator!`.

## Guarantees

- `swap`, `reset`, validator replacement, and compare-and-set are linearizable.
- A swap function runs exactly once while the atom's reentrant lock is held.
- Validators run before commit. Rejection leaves the old value unchanged.
- Watches run synchronously after commit, outside the lock, in registration order.
- A watch exception propagates but never rolls back committed state.
- Compare-and-set and change notification use object identity, not equality.
- Reading an atom is safe; mutating a mutable value obtained from it is not synchronized. Prefer immutable values.

See the [API reference](https://github.com/spork-it/spork-state/blob/main/docs/API.md) and [design semantics](https://github.com/spork-it/spork-state/blob/main/docs/DESIGN.md) for concurrency details.

## Development

Requires `spork-lang` 0.4.0 or newer. The public Spork namespace, Python initializer, generic stubs, version metadata, and `py.typed` are generated from the unified `:api` declaration in `spork.it`; none are maintained as parallel facade files.

```bash
spork sync --dev
spork test
mypy tests/typing/usage.py
spork dist --clean
python -m twine check dist/*
```

## License

MIT
