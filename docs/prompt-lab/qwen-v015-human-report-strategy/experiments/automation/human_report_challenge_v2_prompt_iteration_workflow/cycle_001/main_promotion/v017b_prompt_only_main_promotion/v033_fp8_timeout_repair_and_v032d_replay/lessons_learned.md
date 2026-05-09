# v033 Lessons Learned

- The timeout policy must be experiment-local and explicit.
- Case-level retries are acceptable only when every retry is logged and partial packs remain unscored.
- v032d cannot become FP8 working best without a valid full all-current result below 71 errors.
