# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.2.1] - 2026-08-29

### Changed

- Migrate runtime coverage to native Spork `deftest` declarations, including focused inline helper tests, and remove pytest integration.
- Build and test distributions with `spork-lang` 0.5.0 while requiring only `spork-runtime` from installed packages.

## [0.2.0] - 2026-08-29

### Added

- Package-level Spork API for `(:require [spork-state :as state])`.

### Changed

- Generate both Spork and Python public surfaces from one unified `:api` manifest declaration.
- Require `spork-lang` 0.4.0 or newer.

## [0.1.1] - 2026-08-29

### Changed

- Generate the Python package initializer, version metadata, generic stubs, and `py.typed` directly from `spork.it` and annotated Spork declarations.
- Remove the parallel hand-written Python facade and stub sources.
- Require `spork-lang` 0.3.8 or newer for generated Python APIs and portable postponed annotations.

## [0.1.0] - 2026-08-29

### Added

- Thread-safe `Atom` implementation shared by Spork and Python.
- Atomic reset, swap, value-pair, and identity compare-and-set operations.
- Pre-commit validators and replaceable validator support.
- Synchronous keyed watches and convenient subscriptions.
- Typed Python facade with generic `Atom[T]` stubs.
- Python 3.10–3.14 and free-threaded Python 3.14 support.

[Unreleased]: https://github.com/spork-it/spork-state/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/spork-it/spork-state/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/spork-it/spork-state/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/spork-it/spork-state/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/spork-it/spork-state/releases/tag/v0.1.0
