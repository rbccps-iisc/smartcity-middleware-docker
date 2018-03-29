import urllib
from utils import output_error, output_info, output_ok
import traceback
import os


def download_file(url, filename, success_msg, failure_msg, log_file):
    """ Downloads the file using urllib and prints error and ok message based on the status.

    Args:
        url         (string): url to download
        filename    (string): filename for the downloaded file
        success_msg (string): success message to be displayed when download finishes
        failure_msg (string): failure message to be displayed when download fails
        log_file    (string): log file path
    """
    if os.path.exists(filename):
        output_ok(success_msg)
    else:
        try:
            urllib.urlretrieve(url, filename)
            output_ok(success_msg)
        except Exception:
            output_error(failure_msg + "\n           Check logs {0} for more details.".format(log_file),
                         error_message=traceback.format_exc())
            exit()


def download(log_file):
    """ Download the heavy package files for faster installation into the pkg files.

    Args:
        log_file      (string): log file path
    """
    output_info("Downloading apache-storm-1.1.1.tar.gz")
    download_file("http://www-eu.apache.org/dist/storm/apache-storm-1.1.1/apache-storm-1.1.1.tar.gz",
                  "pkg/apache-storm-1.1.1.tar.gz",
                  "Downloaded apache-storm-1.1.1.tar.gz to pkg directory",
                  "Failure to download apache-storm-1.1.1.tar.gz in pkg directory",
                  log_file)
    output_info("Downloading go1.9.2.linux-amd64.tar.gz")
    download_file("https://storage.googleapis.com/golang/go1.9.2.linux-amd64.tar.gz",
                  "pkg/go1.9.2.linux-amd64.tar.gz",
                  "Downloaded go1.9.2.linux-amd64.tar.gz to pkg directory",
                  "Failure to download go1.9.2.linux-amd64.tar.gz in pkg directory",
                  log_file)
    output_info("Downloading zookeeper-3.4.10.tar.gz")
    download_file("https://apache.org/dist/zookeeper/stable/zookeeper-3.4.10.tar.gz",
                  "pkg/zookeeper-3.4.10.tar.gz",
                  "Downloaded zookeeper-3.4.10.tar.gz to pkg directory",
                  "Failure to download zookeeper-3.4.10.tar.gz in pkg directory",
                  log_file)
