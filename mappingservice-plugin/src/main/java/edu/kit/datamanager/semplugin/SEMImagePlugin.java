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

import org.tomlj.Toml;
import org.tomlj.TomlParseResult;

public class SEMImagePlugin implements IMappingPlugin{

    private static String version;

    private final Logger LOGGER = LoggerFactory.getLogger(SEMImagePlugin.class);
    private String REPOSITORY;
    private String TAG;
    private String NAME;
    private String DESCRIPTION;
    private MimeType[] INPUT_MIME_TYPES;
    private MimeType[] OUTPUT_MIME_TYPES;
    private Path dir;

    public SEMImagePlugin() {
        loadVersion();
        loadTomlConfig();
    }

    private void loadTomlConfig() {
        ClassLoader classLoader = this.getClass().getClassLoader();
        URL resource = classLoader.getResource("pyproject.toml");
        LOGGER.info("Resource file: " + resource);

        if (resource != null) {
            try (InputStream input = resource.openStream()) {
                TomlParseResult result = Toml.parse(input);

                if (result.hasErrors()) {
                    result.errors().forEach(error -> LOGGER.warn("TOML parse error: " + error.toString()));
                } else {
                    REPOSITORY = result.getString("project.urls.repository");
                    if (REPOSITORY == null) throw new IllegalArgumentException("Repository URL cannot be read from config");
                    NAME = result.getString("tool.plugin.name");
                    if (NAME == null) throw new IllegalArgumentException("Plugin name cannot be read from config");
                    DESCRIPTION = result.contains("tool.plugin.description") ? result.getString("tool.plugin.description") : "descrption unavailable";
                    INPUT_MIME_TYPES = result.getArrayOrEmpty("tool.plugin.input_mimes").toList().stream().map(Object::toString).map(MimeTypeUtils::parseMimeType).toArray(MimeType[]::new);
                    OUTPUT_MIME_TYPES = result.getArrayOrEmpty("tool.plugin.output_mimes").toList().stream().map(Object::toString).map(MimeTypeUtils::parseMimeType).toArray(MimeType[]::new);
                }
            } catch (Exception e) {
                LOGGER.error("Failed to load TOML file: " + e.getMessage());
            }
        }
    }

    private void loadVersion() {
        try {
            // Get the context class loader
            ClassLoader classLoader = this.getClass().getClassLoader();
            URL resource = classLoader.getResource("pluginversion.properties");
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
        return NAME;
    }

    @Override
    public String description() {
        return DESCRIPTION;
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
        return new MimeType[]{MimeTypeUtils.parseMimeType("image/tiff"), MimeTypeUtils.parseMimeType("text/plain")};
    }

    @Override
    public MimeType[] outputTypes() {
        return OUTPUT_MIME_TYPES;
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
        LOGGER.trace("Run {} on '{}' with mapping '{}' -> '{}'", this.name(), mappingFile, inputFile, outputFile);
        //MappingPluginState result = PythonRunnerUtil.runPythonScript(dir + "/metaMapper.py", mappingFile.toString(), inputFile.toString(), outputFile.toString());
        String[] args = {"-m", mappingFile.toString(), "-i", inputFile.toString(), "-o", outputFile.toString()};
        MappingPluginState result = PythonRunnerUtil.runPythonScript(dir + "/plugin_wrapper.py", args);
        long endTime = System.currentTimeMillis();
        long totalTime = endTime - startTime;
        LOGGER.info("Execution time of mapFile: {} milliseconds", totalTime);
        return result;
    }
}
