# Rule Spec r019

- containment >= `0.8`
- IoU >= `0.0`
- area ratio <= `0.1`
- center inside larger box required: `True`
- same-label required: `True`
- only suppress if larger box is matched: `True`
- never suppress if smaller box is matched: `True`
- never suppress if both boxes overlap distinct references: `True`
- never suppress if smaller box has better reference IoU: `True`
