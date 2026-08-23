#!/usr/bin/env python3
"""Generate one pre-titled copy of HTF_Candles_Single.pine per timeframe.

Each generated file only differs from the template in its indicator title and
the default value of the "Timeframe" input, so all nine scripts show up in the
TradingView legend under their own name ("HTF Candles 1D", "HTF Candles 4H", …)
with their own eye icon.

    python3 tools/generate_singles.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "HTF_Candles_Single.pine"
OUT_DIR = ROOT / "singles"

# (label shown in the chart legend, timeframe string TradingView expects)
TIMEFRAMES = [
    ("W", "1W"),
    ("D", "1D"),
    ("12h", "720"),
    ("4h", "240"),
    ("1h", "60"),
    ("30m", "30"),
    ("15m", "15"),
    ("5m", "5"),
    ("1m", "1"),
]

TITLE_RE = re.compile(r'^indicator\("HTF Candles", "HTF Candles",', re.MULTILINE)
TF_RE = re.compile(r'^htf(\s*)=\s*input\.timeframe\("[^"]*"(.*//\s*@tf)$', re.MULTILINE)
LABEL_RE = re.compile(r'^tfLabel(\s*)=\s*input\.string\("[^"]*"(.*//\s*@label)$', re.MULTILINE)


def main() -> None:
    template = TEMPLATE.read_text(encoding="utf-8")
    OUT_DIR.mkdir(exist_ok=True)

    for label, tf in TIMEFRAMES:
        # Title and short title are kept identical so the chart legend always
        # reads "HTF Candles <TF>" — that is the row you toggle with the eye.
        src = TITLE_RE.sub(
            f'indicator("HTF Candles {label}", "HTF Candles {label}",', template, count=1
        )
        src, n_tf = TF_RE.subn(
            lambda m: f'htf{m.group(1)}= input.timeframe("{tf}"{m.group(2)}', src, count=1
        )
        src, n_lbl = LABEL_RE.subn(
            lambda m: f'tfLabel{m.group(1)}= input.string("{label}"{m.group(2)}', src, count=1
        )
        if src == template or n_tf != 1 or n_lbl != 1:
            raise SystemExit("template markers not found — did the template change?")

        out = OUT_DIR / f"HTF_Candles_{label}.pine"
        out.write_text(src, encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
