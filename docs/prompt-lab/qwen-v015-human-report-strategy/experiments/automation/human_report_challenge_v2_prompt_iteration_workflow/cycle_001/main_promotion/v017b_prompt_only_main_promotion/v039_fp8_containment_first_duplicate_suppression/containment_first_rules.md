# v039 Containment-First Rules

Rules suppress only an unmatched smaller box that is mostly contained in a larger matched prediction. IoU may be disabled or set below v038's `0.10` floor. A smaller matched box, a distinct-reference pair, or a smaller box with better reference IoU is never suppressed.
