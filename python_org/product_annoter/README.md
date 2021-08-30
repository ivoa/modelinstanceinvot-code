### Product annotation

This package can insert in a VOTABLE an annotation block with all measurements described in a JSON file.

This file is specific to a particular catalog since it contains the FIELD ids and the values matching the model leaves

All the rest of the stuff is catalog independent

The demo program is in the `demo` folder

#### Workfow

- The VOTable to be annotated is located in  `/python_workflow/data/raw_data`
  - Let's assume it is called `my_votable.xml`
  - Rename the `<TABLE>` to be annotated as `Results`. This is the name is set by the mapper. It is not configurable for now.
- The mapping configuration is located in `/python_workflow/data/product_config`. It must be named `my_votable.json`
  - This file contains the list of the Mango parameters (measures) that have to be mapped and how the mapping has to be tuned.
- Write a Python script based on those you can find in `demo` and run it.
```python
% cd demo
% python my_votable-annoter.py
# Lots of output
```
- The output (as long as no error) is stored in `/python_workflow/data/annotated_data`. 
- 2 files are generated
  - `my_votable.mapping.xml` This file just contains the mapping block. Is is quite liter than the whole VOTable which can bee too heavy for text editors.
  - `my_votable.annot.xml` This file contains the whole annotated VOTable.

