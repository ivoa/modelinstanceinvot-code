### Client

This package show how to consume an annotated VOTABLE.

The process is as follow:

1. Extracting the MODEL_INSTANCE block out of the VOTable

2. Convert it in JSON (xmltojson package)

3. Replace the tag names with the matching roles

4. Uses the so created object instance as index to browse the VOTable data.

```shell
% cd demo
% python3 *****.py
```