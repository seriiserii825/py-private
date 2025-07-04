import glob
import os

from libs.selectWithFzf import selectWithFzf


def selectWpressFiles():
    downloads_dir = os.path.expanduser("~/Downloads")
    downloads_dir = os.path.expanduser("~/Downloads")
    wpress_files = glob.glob(f"{downloads_dir}/*.wpress")
    wpress_files.sort(key=os.path.getmtime, reverse=True)
    wpress_files = [os.path.basename(file) for file in wpress_files]
    wpress_file = selectWithFzf(wpress_files)
    return os.path.join(downloads_dir, wpress_file)
