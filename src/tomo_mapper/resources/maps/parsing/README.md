# Tomography Map Files

The map file for tomography mapping is aiming for fine-tuning the mapping for specifics of input data.

- `setup info`: Provide which metadata files to parse for general experiment metadata
- `run info`: Provide metadata files to parse for metadata of experiment results / run
- `image info`: Provide files to parse als image metadata (may be images or separate header files)
- source paths may contain inclusion wildcard patterns (glob syntax)

For more details check out the default maps in this folder:

[Default map for Thermofisher input](inputmap_thermofisher.json)

[Default map for Zeiss input](inputmap_zeiss-auriga.json)

[Default map for Tescan input](./inputmap_tescan-minimal.json) (dataset_info.hdr file only for setup md)

[Extended map for Tescan input](./inputmap_tescan.json) <br>
(additionally reads in an xml setup md file. The file name likely needs to be changed on usage)