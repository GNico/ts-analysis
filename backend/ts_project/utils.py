import os

def get_files_from_directory(filespath):
	return [ os.path.join(filespath,f) for f in os.listdir(filespath) if os.path.isfile(os.path.join(filespath,f)) ]
