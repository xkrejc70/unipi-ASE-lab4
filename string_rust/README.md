# string_rust

A simple microservice implemented in Rust (with [actix](https://actix.rs)) featuring the following four operations on strings:

- `/concat?a=<String>&b=<String>`, to concatenate two strings `a` and `b`,
- `/editdistance?a=<String>&b=<String>`, to compute the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) between strings `a` and `b`,
- `/upper?a=<String>`, to turn string `a` into upper-case
- `/lower?a=<String>`, to turn string `a` into lower-case

Outputs are JSON formatted, like:

```json
{
   "res":"<String>"
}
```