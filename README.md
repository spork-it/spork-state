# spork-state

[![Tests](https://github.com/spork-it/spork-state/actions/workflows/test.yml/badge.svg)](https://github.com/spork-it/spork-state/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/spork-state.svg)](https://pypi.org/project/spork-state/)

`spork-state` provides a thread-safe, validated, observable `Atom` with one Spork implementation and generated typed Python and Spork APIs.

## Install

Python:

```bash
python -m pip install spork-state
```

Spork project manifest:

```clojure
:dependencies ["spork-state>=0.2,<0.3"]
```

Then run `spork sync`.

## Python

```python
from spork_state import Atom

counter = Atom(0, validator=lambda value: value >= 0)
unsubscribe = counter.subscribe(
    lambda old, new: print(f"{old} -> {new}"),
    fire_immediately=True,
)

counter.swap(lambda value, amount: value + amount, 3)
assert counter.value == 3
unsubscribe()
```

## Spork

```clojure
(ns example.counter
  (:require [spork-state :as state]))

(def counter (state.atom 0 (fn [value] (>= value 0))))
(state.swap! counter (fn [value amount] (+ value amount)) 3)
(assert (= (state.deref counter) 3))
```

Updates and validator replacement are linearizable. Validators run before commit. Watches run synchronously after commit, outside the lock, in registration order. Compare-and-set and watch transitions use object identity rather than equality.

## Documentation

- [Package overview](https://spork.sh/docs/packages/spork-state/)
- [Practical guide](https://spork.sh/docs/packages/spork-state/guide/)
- [API reference](https://spork.sh/docs/packages/spork-state/api/)
- [Concurrency design](https://spork.sh/docs/packages/spork-state/design/)
- [Changelog](CHANGELOG.md)

## Development

```bash
spork sync --dev
spork test
mypy tests/typing/usage.py
spork dist --clean
```

## License

MIT. See [LICENSE](LICENSE).
