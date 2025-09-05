import os
import json
import logging
import zipfile

from src.IO.MappingAbortionError import MappingAbortionError


class OutputWriter:

    @staticmethod
    def save_the_file(mapped_metadata, file_path):
        try:
            with open(file_path, 'w', encoding="utf-8") as json_file:
                json.dump(mapped_metadata, json_file, indent=4, ensure_ascii=False)
            logging.info("The output document has been created successfully!")
        except MappingAbortionError as e:
            logging.error(f"Unable to save {file_path}: {e}")
            raise MappingAbortionError(f"Failed to save {file_path}.")

    @staticmethod
    def save_to_zip(file_path_list, zip_file_path):
        try:
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                # "ZIP_DEFLATED" is a lossless compression algorithm, meaning no data is lost during the compression process.
                for file_path in file_path_list:
                    try:
                        zf.write(file_path, os.path.basename(file_path))
                        logging.debug(f"Added {file_path} to zip.")
                    except Exception as e:
                        logging.error(f"Adding {file_path} to zip was not successful: {e}")
                        raise MappingAbortionError(f"Failed to add {file_path} to zip.")
            logging.info(f"Files have been zipped into {zip_file_path} sucessfully!")
        except MappingAbortionError as e:
            logging.error(f"Failed to create zip file at {zip_file_path}: {e}")
            raise MappingAbortionError(f"Failed to save to zip.")
            
        # Delete the original files after zipping
        for file_path in file_path_list:
            try:
                os.remove(file_path)
                logging.info(f"{file_path} has been deleted.")
            except (FileNotFoundError, PermissionError, IsADirectoryError, OSError) as e:
                logging.warning(f"{file_path} to zip was not deleted: {e}")
                raise MappingAbortionError(f"Failed to delete file {file_path} after zip.")
