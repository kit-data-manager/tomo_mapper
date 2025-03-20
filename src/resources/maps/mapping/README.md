# Input - Output Path Mapping

The map file designed for metadata mapping defines the relation between input path and output path in the resulting json.
All read-in information is read in into a json / dict structure for unified mapping definition.

## Map File

All maps are expected to be in a json format with a list of key: value pairs, where key is a string representing a dotted path in the input data, 
and value is a string representing the corresponding dotted path in the output format.

```json
{
  "path.to.input1": "path.to.output1",
  "path.to.input2": "path.to.output2"
}
```

Representation of xml input follows the default behaviour of [xmltodict](https://omz-software.com/pythonista/docs/ios/xmltodict.html), writing attributes to "@<attribute>" and values to "#text" paths.

## Basic Mapping

The mapping definition allows for the following relations:

- 1-to-1: path to a single value on the left to single value on the right (see line 1 and 2 in example below)
- n-to-n: path to a list element on the left is put to a corresponding list element on the right (see line 3 in example below)
- n-to-1: path to list elements on the left is put into a single field on the right. This should usually only be used for duplicate entries that need to be extracted into a single structure (see line 4 in example below)

```json
{
  "path.to.input_value": "path.to.output_value",
  "path.to.input_list[3].value": "path.to.output_value",
  "path.to.input_list[*].value": "path.to.output_list[*].value",
  "path.to.input_list[*].value": "path.to.output_value"
}
```

Type conversion is done automatically and schema-compliant if possible. This functionality mainly remains on the core functionality provided by `pydantic`. 
The conversion strategy is non-strict, for example mapping values like 'off' or 'no' to boolean true/false values, if expected by the output schema.

The internal prepropressing provides additional conversion such as simple mapping of common unit representations. This handling at the moment is by no means complete and may need future extension.

## Advanced mapping

Besides mapping complete input values to an output field, there is often the need to either split the input field or to only capture it partially. 
To allow for this, we utilize the substitution function by the [extension of jsonpath-ng](https://github.com/h2non/jsonpath-ng?tab=readme-ov-file#extensions)
to allow a regex-based definition directly attached to the input path. Make sure to include the backticks, otherwise it will not be recognized as a function attachement.

*Example*

Input:
```
{
    "complex_value": "30.0 with addition"
}
```

Map (regex pattern and capture group):
```
{
    "complex_value.`sub(/(\\d+\\.?\\d?) .+/, \\\\1))`": "captured_value"
}
```

Output:
```
{
    "captured_value": 30.0
}
```

## Mapping Examples

To check out the approach for various vendors and input formats, check out the files in this folder.

### FAQ

**I want to do something more complicated on the data than defined above, how do I do that?**

> The map file approach tries to provide a way to define and document input handling separately and explicitely to help with extension without coding. It is, however, conceptionally limited in its capabilities. 
More complicated parsing likely needs handling in code instead. Feel free to open an issue to discuss further needs.

**The map files define overly complicated input definitions for tiff tags. Why are you even using the raw tiff tags, shouldn't libraries like `tifffile` / `hyperspy` handle those inputs more gracefully and robustly?**

> While utilizing those libraries would provide us with a more high-level approach for the data extraction, all libraries a) only cover specific formats (such as tiff) and b) are not extracting from all input sources with the same level of abstraction.
Currently we opt for the less pretty and more extensible approach, especially since the development heavily relies on sample data. With a more complete picture in the future a rework may be suitable.
