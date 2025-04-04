# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
import requests
import zipfile
import shutil
import logging
import time
import schedule
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_updater.log"),
        logging.StreamHandler()
    ]
)

# Configuration
URL_DOWNLOAD = os.getenv("URL_DOWNLOAD")
TEMP_FOLDER = os.getenv("TEMP_FOLDER")
DATA_FOLDER = os.getenv("SCRUTINS_FOLDER")
UPDATE_HOUR = os.getenv("UPDATE_HOUR")

def download_file(url: str, des_folder: str) -> str | None:
    """TODO"""
    try:
        if not os.path.exists(des_folder):
            os.makedirs(des_folder)
            
        file_name = os.path.join(des_folder, "data.zip")
        logging.info(f"Download from {url}")
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        logging.info(f"Download done {file_name}")
        return file_name
        
    except Exception as e:
        logging.error(f"Error during download: {str(e)}")
        return None

def unzip_file(path: str, des_folder: str) -> str | None:
    """TODO"""
    try:
        if not os.path.exists(des_folder):
            os.makedirs(des_folder)
            
        temp = f"{des_folder}_temp"
        if os.path.exists(temp):
            shutil.rmtree(temp)
        os.makedirs(temp)
        
        logging.info(f"Unzipping file {path}")
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(temp)
            
        logging.info(f"Unzipping done {temp}")
        return temp
        
    except Exception as e:
        logging.error(f"Error during unzipping: {str(e)}")
        return None

def moving_folder(src_folder: str, des_folder: str):
    """TODO"""
    try:
        logging.info(f"Moving all files from {src_folder}")
        all_file = []
        
        # Find all files to be moved
        for root, _, files in os.walk(src_folder):
            for f in files:
                path = os.path.join(root, f)
                all_file.append(path)
        
        logging.info(f"Moving in {des_folder}")
        if not os.path.exists(des_folder):
            os.makedirs(des_folder)

        for src_path in all_file:
            # destination path
            name_file = os.path.basename(src_path)
            des_path = os.path.join(des_folder, name_file)
            
            # removing already existing file
            if os.path.exists(des_path):
                os.remove(des_path)
            
            # copy new file
            shutil.copy2(src_path, des_path)
                
        logging.info(f"Moving done in {des_folder}")
        return True
        
    except Exception as e:
        logging.error(f"Erorr during renaming : {str(e)}")
        return False

def clean(zip_file: str, temp: str | None=None) -> None:
    """TODO"""
    try:
        if os.path.exists(zip_file):
            os.remove(zip_file)
            logging.info(f"Deleted file: {zip_file}")
            
        if temp and os.path.exists(temp):
            shutil.rmtree(temp)
            logging.info(f"Deleted folder: {temp}")
            
    except Exception as e:
        logging.error(f"Error during cleaning: {str(e)}")

def update() -> bool:
    """TODO"""
    logging.info("=== Update starting ===")
    
    zip_file = download_file(URL_DOWNLOAD, TEMP_FOLDER)
    if not zip_file:
        logging.error("Update failed: download failed")
        return False
    
    folder = unzip_file(zip_file, TEMP_FOLDER)
    if not folder:
        clean(zip_file)
        logging.error("Update failed : unzipping failed")
        return False
    
    success = moving_folder(folder, DATA_FOLDER)
    clean(zip_file, folder)
    
    if success:
        logging.info("=== Update success ===")
    else:
        logging.error("=== Update failed ===")
    
    return success

def start_planning():
    """TODO"""
    schedule.every().day.at(UPDATE_HOUR).do(update)
    logging.info(f"Update planed at {UPDATE_HOUR}")
    
    logging.info("First update...")
    update()

    while True:
        schedule.run_pending()
        time.sleep(900)  # Check every 15min

if __name__ == "__main__":
    start_planning()