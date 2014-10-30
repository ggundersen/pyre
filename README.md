Pyre
====
Pyre is a Python implementation of a regular expression engine.

Valid operators
---------------
- Boolean "or" denoted by "|". For example, `foo|bar` would match the words "foo" or "bar".
- Concatenation is implicit. For example, `foo` is actually the concatentation of "f", "o", and "o".
- Kleene star denoted by "\*". For example, f\*o would match zero or more "f"s, followed by a single "o".

How to run
----------
Currently, Pyre is a command line tool. To run, execute `pyre.py` followed by the regular expression and then the string you'd like to match.

For example:
`python3 pyre.py a+b aab`
