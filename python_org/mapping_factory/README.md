# Mapping Factory

This package contains tools able to extract model components from MODEL_INSTANCE files.

. Concrete class and types can be specified from specific role (*)

. Generated mapping blocks are just printed out, they must be pasted in files to stored in `data/mapping_components`

. In some cases, blocks might have to be patched by hand

. This package includes a XSD mapping validator.

(*) with some bugs: ONe concrete class can not be overloaded mor than once 

```shell
% cd launchers
% python3 transform_****
```