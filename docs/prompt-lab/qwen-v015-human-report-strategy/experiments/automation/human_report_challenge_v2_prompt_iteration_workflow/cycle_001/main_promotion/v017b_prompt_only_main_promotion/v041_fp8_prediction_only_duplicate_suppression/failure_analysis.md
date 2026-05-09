# v041 Failure Analysis

- Safe rules: `34520`.
- Best rule removed true positives: `0`.
- Best rule matched r020/hybrid: `False`.
- Best rule matched r019: `False`.
- Cross-label suppression acceptable for selected rule: `True`.
- Rules that fixed case 155: `21900`; safe case-155-fixing rules: `8480`.
- Rules that removed both case 88 and case 155: `6600`; safe rules removing both: `0`.
- Main de-oracle loss mode: case 155 is separable as a one-FP safe rule, but combining case 88 and 155 without oracle checks also catches a case-159 true positive.
