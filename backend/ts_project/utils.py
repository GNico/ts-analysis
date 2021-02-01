import os
from django.conf import settings

def get_data_source_path():
	return settings.ELASTIC_DATA_INDEX_PATH

def get_dirs_from_dir(dir_path):
	return [ f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path,f)) and f[0] != '.']

def get_files_from_directory(files_path):
	return [ os.path.join(files_path,f) for f in os.listdir(files_path) if os.path.isfile(os.path.join(files_path,f)) ]
