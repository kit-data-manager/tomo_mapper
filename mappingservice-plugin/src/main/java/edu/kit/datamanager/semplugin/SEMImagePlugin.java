package edu.kit.datamanager.semplugin;

import edu.kit.datamanager.mappingservice.plugins.AbstractPythonMappingPlugin;
import java.nio.file.Path;

public class SEMImagePlugin extends AbstractPythonMappingPlugin {

   private static final String REPOSITORY = "https://github.com/kit-data-manager/tomo_mapper";


    public SEMImagePlugin() {
        super("GenericSEMtoJSON", REPOSITORY);
    }

    @Override
    public String name() {
        return "GenericSEMtoJSON";
    }

    @Override
    public String description() {
        return "This python based tool extracts metadata from machine generated scanning microscopy images and generates a JSON file adhering to the schema.";
    }

    @Override
    public String[] inputTypes() {
        return new String[]{"image/tiff", "text/plain"};
    }

    @Override
    public String[] outputTypes() {
        return new String[]{"application/json"};
    }

    @Override
    public String[] getCommandArray(Path workingDir, Path mappingFile, Path inputFile, Path outputFile) {
        return new String[]{
                workingDir + "/plugin_wrapper.py",
                "sem",
                "-m",
                mappingFile.toString(),
                "-i",
                inputFile.toString(),
                "-o",
                outputFile.toString()
        };
    }
}
