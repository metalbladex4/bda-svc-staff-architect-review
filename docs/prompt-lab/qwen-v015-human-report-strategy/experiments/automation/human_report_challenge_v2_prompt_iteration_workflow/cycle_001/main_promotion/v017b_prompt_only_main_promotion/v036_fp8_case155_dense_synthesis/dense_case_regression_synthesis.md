# Dense Case Regression Synthesis

v035a hurt dense rows because its added wording was too broad. Case 67 fell from `10/1/3` to `7/4/5`, creating four FNs and five FPs. Case 66 retained recall but added one FP, moving from `8/0/5` to `8/0/6`. Case 84 remained weak at `8/5/0`, so the candidate did not repair dense recall.

The likely load-bearing phrase was: `isolated dense-scene marks or partial fragments when the target body center and exterior boundary are not both visible`. This appears to have shifted the model toward rejecting valid small/crowded targets rather than only rejecting the nested case-155 local duplicate.

Future candidates should ban the terms `dense-scene`, `partial fragments`, `uncertain fragments`, `body center and exterior boundary`, and `isolated marks` for this axis.
