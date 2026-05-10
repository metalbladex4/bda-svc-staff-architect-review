# Tiling Strategy

|strategy|name|crop_generation_without_ground_truth|intended_recovery|fp_risk|
|---|---|---|---|---|
|A|full-image 2x2 overlap|four 62 percent image tiles anchored at image corners|building pieces, dense/small targets, smoke/debris targets|medium|
|B|generic dense-row strips|middle-lower and lower full-width strips from image geometry only|dense row and lower-band small objects|medium_high|
|C|prediction-anchored neighbor crops|padded crops around the three largest locked baseline detections|adjacent target confusion|medium_high|
|D|smoke/debris broad context crop|single centered 84 percent image crop|smoke/debris-obscured and broad context misses|medium|
