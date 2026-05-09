# v042 Postprocessing Wrapper

The wrapper is experiment-only. It applies `p1753` to saved prediction JSON files, writes postprocessed copies, and scores raw plus postprocessed outputs. The rule itself uses only prediction geometry and target type labels; ground truth is used only after suppression for evaluation/audit.
