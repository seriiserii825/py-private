import glob
import os

from classes.FilesHandle import FilesHandle
from classes.utils.Select import Select
from libs.selectWithFzf import selectWithFzf


def selectWpressFiles():
    fh = FilesHandle()
    downloads_dir = os.path.expanduser("~/Downloads")
    fh.list_files(path_to_list=downloads_dir,
                  file_extension=".wpress", mtime=True)
    wpress_files = glob.glob(f"{downloads_dir}/*.wpress")
    wpress_files.sort(key=os.path.getmtime, reverse=True)
    wpress_files = [os.path.basename(file) for file in wpress_files]
    wpress_file = Select.select_one(wpress_files)
    wpress_file = downloads_dir + "/" + wpress_file
    return os.path.join(wpress_file)
