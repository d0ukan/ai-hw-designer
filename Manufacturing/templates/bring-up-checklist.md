# <prefix> — Bring-up and test checklist (VER-09)

Go in order when powering the board for the first time. Write the result and the measured value of each step; a step not done stays "not verified".

| # | Step | Expected | Measured / result |
| :--- | :--- | :--- | :--- |
| 1 | Visual check: bridges, reversed parts, missing parts, polarity | No faults | |
| 2 | Supply–GND resistance before power-up (each rail) | No short circuit | |
| 3 | First power-up from a current-limited supply (low limit) | Expected idle current | |
| 4 | Voltage and ripple of each supply rail | Design value ± tolerance | |
| 5 | Check for hot parts (touch/thermal camera) | No abnormal heating | |
| 6 | Reset, clock (crystal/oscillator) | Working | |
| 7 | Programming/debug connection (if any) | Connects | |
| 8 | Interface and function tests (INT-24 acceptance criteria) | Passed | |
| 9 | Battery/charging tests, if any (BAT-08) | Passed | |
| 10 | Record the results in `REVIEW_LOG.md` and the `Project-README.md` checkpoint | Recorded | |
