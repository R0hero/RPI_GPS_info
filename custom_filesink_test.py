"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

# filesize: 12.288e09
# filename: '/home/benja/Dropbox/Uni/Semester 11/Specialkursus/Scripts/grc_test_file_custom.bin' (while testing)

import os
import numpy as np
import shutil
import datetime
from gnuradio import gr

class CustomFileSink(gr.sync_block):
    def __init__(self, filename="/home/benja/Dropbox/Uni/Semester 11/Specialkursus/Scripts/grc_test_file_custom.bin", max_file_size=12.288e09):
        gr.sync_block.__init__(
            self,
            name="Custom File Sink",
            in_sig=[(np.complex64)],
            out_sig=[],
        )
        self.filename = filename
        self.max_file_size = max_file_size
        self.current_file_size = 0
        self.current_file_index = 1
        self.current_file = None

    def work(self, input_items, output_items):
        data = input_items[0]
        if not self.current_file:
            self.current_filename = f"{self.filename[:-4]}_{self.current_file_index}{self.filename[-4:]}"
            if not os.path.exists(self.current_filename):
            	with open(self.current_filename, "w"):
            		pass
            self.current_file = open(self.current_filename, "wb")

        for item in data:
            item_bytes = item.tobytes()
            self.current_file.write(item_bytes)
            self.current_file_size += len(item_bytes)

            if self.current_file_size >= self.max_file_size / 10:
                self.current_file.close()
                self.current_file_index += 1
                new_filename = f"{self.filename[:-4]}_{self.current_file_index}{self.filename[-4:]}"
                if not os.path.exists(new_filename):
                    with open(new_filename, "w"):
                        pass
                self.current_file = open(new_filename, "wb")
                self.current_file_size = 0

            if self.current_file_index == 10:
            	self.current_file_index = 0


        return len(input_items[0])




