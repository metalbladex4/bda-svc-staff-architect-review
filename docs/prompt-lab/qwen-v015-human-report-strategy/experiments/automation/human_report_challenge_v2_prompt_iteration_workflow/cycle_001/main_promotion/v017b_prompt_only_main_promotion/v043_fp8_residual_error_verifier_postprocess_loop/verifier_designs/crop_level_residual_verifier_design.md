# Crop-Level Residual Verifier Design

This design is experiment-only. It targets residual FPs that prediction-only geometry cannot safely separate, especially adjacent-target confusion, broad context boxes, and building/structure pieces.

The verifier should receive a crop, the full overlay, the candidate target type, and neighbor-box context, then emit a small JSON decision. Dense cases require a conservative keep/needs-review bias rather than automatic suppression.
