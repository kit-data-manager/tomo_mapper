package edu.kit.datamanager.semplugin;

import edu.kit.datamanager.mappingservice.plugins.*;
import edu.kit.datamanager.mappingservice.util.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.PropertySource;
import org.springframework.util.MimeType;
import org.springframework.util.MimeTypeUtils;

import java.nio.file.Path;

@PropertySource("classpath:sempluginversion.properties")
public class SEMImagePlugin implements IMappingPlugin{

    @Value( "${version}" )
    private static String version;

    private final Logger LOGGER = LoggerFactory.getLogger(SEMImagePlugin.class);
    private static final String REPOSITORY = "https://github.com/kit-data-manager/tomo_mapper";
    //private static final String TAG = String.join("v", version);
    private static final String TAG = "wip_semmapping";
    private static Path dir;

    @Override
    public String name() {
        return "GenericSEMtoJSON";
    }

    @Override
    public String description() {
        return "This python based tool extracts metadata from machine generated scanning microscopy images and generates a JSON file adhering to the schema.";
    }

    @Override
    public String version() {
        return version;
    }

    @Override
    public String uri() {
        return REPOSITORY;
    }

    @Override
    public MimeType[] inputTypes() {
        return new MimeType[]{MimeTypeUtils.ALL}; //should currently be IMAGE/TIFF
    }

    @Override
    public MimeType[] outputTypes() {
        return new MimeType[]{MimeTypeUtils.APPLICATION_JSON};
    }

    @Override
    public void setup() {
        LOGGER.info("Checking and installing dependencies for the tool: ");
        //TODO: test for minimal python version?
        try {

            dir = FileUtil.cloneGitRepository(REPOSITORY, TAG);
            // Install Python dependencies

            ProcessBuilder pb = new ProcessBuilder("python3", "-m", "pip", "install", "-r", dir + "/requirements.txt");
            pb.inheritIO();
            Process p = pb.start();

            int exitCode = p.waitFor();
            if (exitCode != 0) {
                LOGGER.error("Failed to install Python packages");
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public MappingPluginState mapFile(Path mappingFile, Path inputFile, Path outputFile) throws MappingPluginException {
        long startTime = System.currentTimeMillis();
        LOGGER.trace("Run SEM-Mapping-Tool on '{}' with mapping '{}' -> '{}'", mappingFile, inputFile, outputFile);
        //MappingPluginState result = PythonRunnerUtil.runPythonScript(dir + "/metaMapper.py", mappingFile.toString(), inputFile.toString(), outputFile.toString());
        String[] args = {"sem", "-m", mappingFile.toString(), "-i", inputFile.toString(), "-o", outputFile.toString()};
        MappingPluginState result = PythonRunnerUtil.runPythonScript(dir + "/plugin_wrapper.py", args);
        long endTime = System.currentTimeMillis();
        long totalTime = endTime - startTime;
        LOGGER.info("Execution time of mapFile: {} milliseconds", totalTime);
        return result;
    }
}
