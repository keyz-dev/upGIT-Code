import os
from app.utils.constants import logger
from app.controllers import file as file_controller

"""add a to-be-deleted array that contains the dir_paths of all the chunks to be deleted after commit"""

to_be_deleted = []
main_dir = None
max_filesize = 1 * 1024 * 1024
def organize_push_files(dir_path, folder_id, subdir=False):
    global to_be_deleted
    global main_dir
    global max_filesize
    
    try:
        if not subdir:
            main_dir = dir_path 
        file_list = os.listdir(dir_path)
        
        for file in file_list:
            if file == ".git":
                continue
            file_path = os.path.join(dir_path, file)  
            if os.path.isdir(file_path):
                organize_push_files(file_path, folder_id, subdir=True)
            
            # check file size
            
            file_size = os.path.getsize(file_path)
            if file_size > max_filesize:
                filename = os.path.basename(file_path)
                chunk_dir = os.path.dirname(file_path)
                
                """ignore the file"""
                gitignore_path = os.path.join(os.path.dirname(file_path), '.gitignore')
                with open(gitignore_path, 'a') as gitignore_file:
                    gitignore_file.write(f"{filename}\n")
                
                """split the file"""
                chunk_folder_name = os.path.splitext(filename)[0].capitalize() + os.getenv('CHUNK_SUFFIX')
                chunk_dir = os.path.join(chunk_dir, chunk_folder_name)
                if not os.path.exists(chunk_dir):
                    os.mkdir(chunk_dir)
                
                to_be_deleted.append(chunk_dir)
                # chunk size should be 75% of max file size
                chunk_size = int(0.75 * max_filesize)
                split(file_path, chunk_dir, chunk_size)
                
                """save file to db"""
                file_object = {
                    'name': filename,
                    'repo_id': folder_id,
                    'size': file_size,
                    'filepath': file_path
                }
                file_controller.save(file_object)
                    
        return to_be_deleted
    except Exception as e:
        logger.error(f"An error occurred while organizing files: {e}")
        return None

def split(filepath, chunk_dir, chunk_size):
    with open(filepath, 'rb') as file:
        chunk_number = 1
        while chunk := file.read(chunk_size):
            chunk_name = os.path.basename(filepath) + f"part_{chunk_number}"
            with open(os.path.join(chunk_dir, chunk_name), 'wb') as chunk_file:
                chunk_file.write(chunk)
            chunk_number += 1
        # log the progress
        logger.info(f"{chunk_number-1} chunks of {os.path.basename(filepath)} have been created")

def organize_pull_files(dir_path, subdir=False):
    try:
        global main_dir
        global to_be_deleted
        if not subdir:
            main_dir = dir_path
        filelist = os.listdir(dir_path)
        folders = [file for file in filelist if os.path.isdir(os.path.join(dir_path, file)) and file != '.git']
        
        for folder in folders:
            if folder.endswith(os.getenv('CHUNK_SUFFIX')):
                """add folder path to the to-be-deleted list and merget the contents"""
                merged_filename = folder.replace(os.getenv('CHUNK_SUFFIX'), '')
                chunk_dir = os.path.join(dir_path, folder)
                chunk_files = os.listdir(chunk_dir)
                # Get the filename extension
                chunk_file = chunk_files[0]
                chunk_file_ext = os.path.splitext(chunk_file)[1]
                chunk_file_ext = chunk_file_ext.split('part')[0]
                merged_filename = merged_filename + '(merged)'+ chunk_file_ext
                merged_filepath = os.path.join(dir_path, merged_filename)
                
                for chunk_file in chunk_files:
                    chunk_file_path = os.path.join(chunk_dir, chunk_file)
                    with open(chunk_file_path, 'rb') as chunk_file:
                        with open(merged_filepath, 'ab') as file:
                            file.write(chunk_file.read())
                to_be_deleted.append(chunk_dir)
                logger.info(f"successfully merged {folder} chunks")
            else:
                organize_pull_files(os.path.join(dir_path, folder), subdir=True)
        return to_be_deleted
    except Exception as e:
        logger.error(f"An error occurred while organizing files: {e}")
        return None    