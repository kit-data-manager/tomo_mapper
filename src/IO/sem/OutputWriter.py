import os
import json
import logging
import zipfile


class OutputWriter:

    @staticmethod
    def save_the_file(mapped_metadata, file_path):
        try:
            with open(file_path, 'w', encoding="utf-8") as json_file:
                json.dump(mapped_metadata, json_file, indent=4, ensure_ascii=False)
            logging.info(f"{file_path} has been created successfully!")
        except Exception as e:
            logging.error(f"Failed to save {file_path}: {e}")

    @staticmethod
    def save_to_zip(file_path_list, zip_file_path):
        try:
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                # "ZIP_DEFLATED" is a lossless compression algorithm, meaning no data is lost during the compression process.
                for file_path in file_path_list:
                    zf.write(file_path, os.path.basename(file_path))
            logging.info(f"Files have been zipped into {zip_file_path} sucessfully!")
            
            # Delete the original files after zipping
            for file_path in file_path_list:
                os.remove(file_path)
                logging.info(f"{file_path} has been deleted.")

        except Exception as e:
            logging.error(f"Failed to save to zip or delete files: {e}")