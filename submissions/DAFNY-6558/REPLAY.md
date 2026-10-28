# Dafny #6558 — Source-pinned replay

Return to the [case study](README.md) for claims, attribution, and limitations.
These commands are a replay recipe assembled from the pinned source and CLI
definitions, **not a transcript of a new execution or the original author's
complete command history**. No raw historical CSV archive is included here.

## Environment and revision

Use Bash on x86-64 Ubuntu 24.04, Git, Make, unzip, Python 3, .NET SDK 8.0.408,
and Z3 4.16.0. The [pinned root Makefile][root-make] supplies the Ubuntu solver
download and solution build; [global.json][global] permits the .NET 8 feature
band used in the PR. Follow the [upstream build instructions][install] for
other prerequisites, but use the pinned Makefile's solver version rather than
the older version still named in the wiki. Runtime checks also require the
Python, Node.js, Go, Java/Gradle, and C# backend dependencies.

```bash
set -euo pipefail
git clone https://github.com/dafny-lang/dafny.git dafny-6558
cd dafny-6558
git checkout --detach de36f2ec1f9c530080eff7929ae28229f45da069
git submodule update --init --recursive
make z3-ubuntu
make exe

DAFNY=(dotnet "$PWD/Binaries/Dafny.dll")
DAFNY_Z3="$PWD/Binaries/z3/bin/z3-4.16.0"
git rev-parse HEAD
dotnet --version
"$DAFNY_Z3" --version
"${DAFNY[@]}" --version
cd Source/DafnyStandardLibraries
mkdir -p build/ledger-6558
```

Record these outputs and the OS/backend versions with any new results. The
historical report used a checkout-built CLI labeled `4.11.1+b3324a3` while
checking the contents committed as `16f82c9`; a CLI freshly built at the merge
has different build provenance. This recipe makes no promise of identical
resource counts or package archive bytes on another build.

## Verify the package and focused proofs

The following uses the same verified core-package command path as the
[standard-library Makefile][stdlib-make]. It does not run full `make verify`.
The compiler built above embeds the checked-in packages from the pinned merge.
Compare the regenerated package's unpacked contents before interpreting the
package-backed examples as evidence for that regenerated package.

```bash
"${DAFNY[@]}" build -t:lib --hidden-no-verify=false \
  src/Std/dfyconfig.toml --solver-path "$DAFNY_Z3" \
  --output:build/ledger-6558/DafnyStandardLibraries.doo \
  --log-format "csv;LogFileName=build/ledger-6558/package.csv" \
  2>&1 | tee build/ledger-6558/package.log
unzip -q build/ledger-6558/DafnyStandardLibraries.doo \
  -d build/ledger-6558/regenerated
unzip -q binaries/DafnyStandardLibraries.doo \
  -d build/ledger-6558/checked-in
diff -ru build/ledger-6558/checked-in build/ledger-6558/regenerated
```

Expected: zero verification errors. The historical package build reported
2,347 verified units / 7,963 passed CSV batches, including a large unchanged
Base64 obligation. If the content comparison differs, inspect and record the
difference; do not silently substitute a package or claim a match. Archive
SHA-256 alone is not an unpacked-content comparison.

Construct a focused examples project from the [upstream options][example-config],
including only `StringsExamples.dfy` and enabling both assumption warnings:

```bash
python3 - <<'PY'
from pathlib import Path
source = Path("examples/dfyconfig.toml").read_text()
source = source.replace("warn-redundant-assumptions = false",
                        "warn-redundant-assumptions = true")
Path("build/ledger-6558/examples.toml").write_text(
    'includes = ["../../examples/StringsExamples.dfy"]\n' + source)
PY

for seed in {0..9}; do
  "${DAFNY[@]}" measure-complexity src/Std/dfyconfig.toml \
    --filter-position=Strings.dfy --mutations=1 --random-seed="$seed" \
    --solver-path "$DAFNY_Z3" \
    --log-format "csv;LogFileName=build/ledger-6558/strings-$seed.csv" \
    2>&1 | tee "build/ledger-6558/strings-$seed.log"
  "${DAFNY[@]}" measure-complexity build/ledger-6558/examples.toml \
    --mutations=1 --random-seed="$seed" --solver-path "$DAFNY_Z3" \
    --log-format "csv;LogFileName=build/ledger-6558/examples-$seed.csv" \
    2>&1 | tee "build/ledger-6558/examples-$seed.log"
done
```

The [measure-complexity implementation][complexity] supports these seed,
mutation, and file-filter options. Each invocation is a fresh process with one
mutation; `--mutations=10` would instead derive later seeds internally. The
[Strings project][source-config] retains its 5,000,000 resource limit; examples
retain 1,000,000. Do not raise either limit to obtain a pass.

Expected: every selected batch passes, with no verification errors; inspect all
warnings. Historical counts are 55 Strings batches and 13 example/refinement
batches per seed. A different count, warning, failure, or limit must be reported
with the actual command and environment, not folded into the historical totals.

## Summarize fresh resource measurements

The pinned [CSV logger][csv] records per-batch outcomes and resource counts.
Sum the resources for each seed first, then take the median of the ten totals:

```bash
python3 - <<'PY'
import csv
import statistics
from pathlib import Path

root = Path("build/ledger-6558")
for scope, limit in (("strings", 5_000_000), ("examples", 1_000_000)):
    totals, batches, peak = [], 0, 0
    for seed in range(10):
        with (root / f"{scope}-{seed}.csv").open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        assert rows, (scope, seed, "empty results")
        assert all(r["TestResult.Outcome"] == "Passed" for r in rows), (scope, seed)
        # The pinned result logger omits seed zero; CSV then writes "unknown".
        assert all(r["RandomSeed"] == str(seed) or
                   (seed == 0 and r["RandomSeed"] == "unknown")
                   for r in rows), (scope, seed)
        resources = [int(r["TestResult.ResourceCount"]) for r in rows]
        assert max(resources) <= limit, (scope, seed, "resource limit exceeded")
        totals.append(sum(resources))
        batches += len(rows)
        peak = max(peak, max(resources))
    print(scope, "passed batches:", batches, "peak:", peak,
          "median total:", statistics.median(totals))
PY
```

For a new before/after comparison, repeat the recipe in separate clean checkouts
at `b3324a3ba77803d3ff5daa22d876b639bcc1147f` and
`16f82c91df5e400c9f95fab05739635665bd9589`, keeping SDK, solver, options, seeds,
and platform fixed. Build each checkout's CLI so that examples consume that
revision's own embedded packages. Record both CLI versions and any package
comparison differences. This is a new remeasurement, not recovery of the
historical CLI binary or CSV files. Calculate percentage reduction as
`100 * (before_median - after_median) / before_median`. The published inputs yield
10.8% and 86.0% after rounding to one decimal place. The example workload changed
when redundant tests were removed, so this is not an equal-workload runtime
benchmark.

## Runtime and optional package checks

With backend dependencies installed, run the focused file against each target:

```bash
for target in py js go java cs; do
  mkdir -p "build/ledger-6558/runtime-$target"
  "${DAFNY[@]}" test "-t:$target" build/ledger-6558/examples.toml \
    --solver-path "$DAFNY_Z3" \
    --output:"build/ledger-6558/runtime-$target/strings" \
    2>&1 | tee "build/ledger-6558/runtime-$target.log"
done
```

Expected: eight existing runtime tests per target, 40 executions total. The
added round-trip and binary-refinement lemmas are proof examples, not additional
runtime tests. The reported C# run required directly building the emitted C#
project and running its assembly after a nested SDK `Process.GetStat` failure.
If that occurs, retain the failed command's log and record the exact generated
project path, direct build/run commands, warnings, and exit codes separately;
do not report the original `dafny test` command as successful.

The [target-specific Makefile][target-make] provides an additional check:

```bash
make -C src/Std/TargetSpecific check-binary-all NO_VERIFY=false
```

This rebuilds/verifies and compares the six `notarget/cs/java/js/go/py` packages
using the checkout CLI. It is separate from the focused proof loop and runtime
tests. Neither these commands nor the historical package report establishes a
completed full compiler, language-server, or bounded full-library test suite.

[root-make]: https://github.com/dafny-lang/dafny/blob/de36f2ec1f9c530080eff7929ae28229f45da069/Makefile
[global]: https://github.com/dafny-lang/dafny/blob/de36f2ec1f9c530080eff7929ae28229f45da069/global.json
[install]: https://github.com/dafny-lang/dafny/wiki/INSTALL#building-and-developing-from-source-code
[stdlib-make]: https://github.com/dafny-lang/dafny/blob/de36f2ec1f9c530080eff7929ae28229f45da069/Source/DafnyStandardLibraries/Makefile
[source-config]: https://github.com/dafny-lang/dafny/blob/de36f2ec1f9c530080eff7929ae28229f45da069/Source/DafnyStandardLibraries/src/Std/dfyconfig.toml
[example-config]: https://github.com/dafny-lang/dafny/blob/de36f2ec1f9c530080eff7929ae28229f45da069/Source/DafnyStandardLibraries/examples/dfyconfig.toml
[complexity]: https://github.com/dafny-lang/dafny/blob/de36f2ec1f9c530080eff7929ae28229f45da069/Source/DafnyDriver/Commands/MeasureComplexityCommand.cs
[csv]: https://github.com/dafny-lang/dafny/blob/de36f2ec1f9c530080eff7929ae28229f45da069/Source/DafnyDriver/CSVTestLogger.cs
[target-make]: https://github.com/dafny-lang/dafny/blob/de36f2ec1f9c530080eff7929ae28229f45da069/Source/DafnyStandardLibraries/src/Std/TargetSpecific/Makefile
