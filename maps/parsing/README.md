# Parser Maps explained

very preliminary information, subject to change

'''
{
    "acquisition info": {
        "sources": [
            "./EMProject.emxml" #specify at least one path to a metafile
        ],
        "parser": "EMProjectParser"
    },
    "image info": {
        "sources": [
            "./Images/**/*.tif" #specify at least one path to the relevant image files
        ],
        "autodetect_datasets": true, #if set to false, each source will be considered as one dataset, otherwise the datasets will be derived from image detectors
        "tags": ["3875"], #specify at least one tag address to get image metadata from
        "map": "./map_Zeiss.json"
    }
}
'''