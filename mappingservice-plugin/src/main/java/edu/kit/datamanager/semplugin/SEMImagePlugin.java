package edu.kit.datamanager.semplugin;

import edu.kit.datamanager.mappingservice.plugins.*;
import edu.kit.datamanager.mappingservice.util.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.util.MimeType;
import org.springframework.util.MimeTypeUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Path;
import java.util.Properties;

public class SEMImagePlugin implements IMappingPlugin{

    private static String version;

    private final Logger LOGGER = LoggerFactory.getLogger(SEMImagePlugin.class);
    private final String REPOSITORY = "https://github.com/kit-data-manager/tomo_mapper";
    private String TAG;
    private Path dir;


    public SEMImagePlugin() {
        try {
            // Get the context class loader
            ClassLoader classLoader = this.getClass().getClassLoader();
            // TODO: do we need to make sure that the resource path is somehow related to the current plugin to avoid loading the wrong property file in case of identical property names?
            URL resource = classLoader.getResource("sempluginversion.properties");
            LOGGER.info("Resource file: {}", resource);
            if (resource != null) {
                // Load the properties file
                try (InputStream input = resource.openStream()) {
                    Properties properties = new Properties();
                    properties.load(input);
                    version = properties.getProperty("version");
                    TAG = version;
                }
            } else {
                System.err.println("Properties file not found!");
                version = "unavailable";
                TAG = "unavailable";
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
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
    public String version() {
        return version;
    }

    @Override
    public String uri() {
        return REPOSITORY;
    }

    @Override
    public MimeType[] inputTypes() {
        return new MimeType[]{MimeTypeUtils.parseMimeType("image/tiff")}; //should currently be IMAGE/TIFF
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
            LOGGER.info("Cloning git repository {}, Tag {}", REPOSITORY, TAG);
            dir = FileUtil.cloneGitRepository(REPOSITORY, TAG);
            // Install Python dependencies

            ProcessBuilder pb = new ProcessBuilder("python3", "-m", "pip", "install", "-r", dir + "/requirements.dist.txt");
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
