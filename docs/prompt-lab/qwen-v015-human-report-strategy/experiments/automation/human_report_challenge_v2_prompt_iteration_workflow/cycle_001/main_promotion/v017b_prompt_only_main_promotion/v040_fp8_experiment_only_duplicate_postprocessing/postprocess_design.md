# v040 Postprocess Design

The wrapper loads frozen v034a predictions, computes pair geometry against the frozen baseline match map, writes postprocessed copies under `tables/postprocessed_predictions/<rule>/`, and evaluates those copies with the same local `bda_eval` detection-study matching behavior. It is experiment-only and does not modify product runtime.
