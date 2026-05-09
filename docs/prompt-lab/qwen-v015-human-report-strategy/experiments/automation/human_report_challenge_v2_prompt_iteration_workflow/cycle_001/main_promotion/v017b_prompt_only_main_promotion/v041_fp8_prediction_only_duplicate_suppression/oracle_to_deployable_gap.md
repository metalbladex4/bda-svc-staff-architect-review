# v041 Oracle-To-Deployable Gap

v039/v040 proved that containment-first duplicate suppression can reduce FP8 false positives, but the strongest rules used oracle fields: matched/unmatched state, larger-box matched status, distinct-reference overlap, and best reference IoU. Those fields are valid for offline simulation but unavailable at inference time.

v041 therefore restricts rule logic to prediction-only information: predicted boxes, target types, geometry, area ratios, containment, pairwise IoU, center-inside relation, image dimensions, and prediction labels/order. Reference and match data are used only after suppression to score the result and audit whether the rule removed a true positive.
