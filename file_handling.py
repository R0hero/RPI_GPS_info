import os
import datetime
import numpy as np
import shutil

def get_filenames():
    filenames_indexed = []
    for i in range(1,11):
        filenames_indexed.append(f'{FILE_PATH+FILENAME[:-4]}_{i}{FILENAME[-4:]}')
    return filenames_indexed

def main():

    filenames_indexed = get_filenames()

    # set initial conditions
    cond = False
    executed_prev_files = False

    i = 1
    while True:
        # search through filesizes to find which file is being written to
        for j in range(1,11):
            try:        
                filesize = os.path.getsize(filenames_indexed[j-1])
            except FileNotFoundError:
                # if file is not found, set max filesize
                filesize = MAX_FILESIZE//10

            if filesize < MAX_FILESIZE//10:
                current_index = j

        # set condition based on index - only for testing
        if current_index == 4 and not cond:
            cond = True
        
        if cond and not executed_prev_files:
            # check if current_time variable exists and only create it once
            if 'current_time' not in locals():
                current_time = datetime.datetime.now()
            
            # only create directory if it doesn't exist already
            if not os.path.isdir(f'{FILE_PATH}{current_time}'):
                os.mkdir(f'{FILE_PATH}{current_time}')
            
            index_older_files = np.zeros(5,dtype=np.int8)
            # find 5 latest files before incidence
            for i in range(1,6):
                index_older_files[i-1] = current_index - i
                # ensure loop to start over when reaching 1
                if index_older_files[i-1] < 1:
                    index_older_files[i-1] = index_older_files[i-1] + 10
            
            # copy files to folder
            for i in range(len(index_older_files)):
                sorted_filename = f'{FILE_PATH}{current_time}{os.sep}sorted_incidence_{i+1}.bin'
                current_filename = f'{FILE_PATH}{FILENAME[:-4]}_{index_older_files[i]}{FILENAME[-4:]}'
                shutil.copy(current_filename, sorted_filename)

            # set conditions for future work in script
            executed_prev_files = True
            incidence_index = current_index

        # see earlier if statement has been run
        if 'incidence_index' in locals() and executed_prev_files:
            # set remaining index names
            sorted_idx_names = np.array((6,7,8,9,10,11))

            for i in range(0,6):
                sorted_filename = f'{FILE_PATH}{current_time}{os.sep}sorted_incidence_{sorted_idx_names[i]}.bin'
                current_file_idx = incidence_index+i
                # ensure current file index does not exceed 10
                if current_file_idx > 10:
                    current_file_idx -= 10
                
                current_filename = f'{FILE_PATH}{FILENAME[:-4]}_{current_file_idx}{FILENAME[-4:]}'
                
                # see if the current index of file written to is the correct based on filename
                if current_index - incidence_index == i:
                    # only copy if filesize is the maximum allowed
                    if os.path.getsize(current_filename) == MAX_FILESIZE // 10:
                        print(current_file_idx) # debugging
                        shutil.copy(current_filename, sorted_filename)

                        print('copied') # debugging

                # see how many files there are in the folder
                listed_dir = os.listdir(f'{FILE_PATH}{current_time}')
                # check if the final file has been copied to the folder
                if current_index - incidence_index == 5 and len(listed_dir) == 11:
                    # reset conditions
                    executed_prev_files = False
                    cond = False
                    del incidence_index
                    del current_time

                    # set filename generation to search through for merging files
                    sorted_filenames = f'{FILE_PATH}{current_time}{os.sep}sorted_incidence_'
                    sorted_filenames_file_extension = f'.bin'
                    output_filename = f'{FILE_PATH}{current_time}{os.sep}incidence.log'
                    # merge files
                    with open(output_filename, 'wb') as output_file:
                        for i in range(1,12):
                            current_filename = f'{sorted_filenames}{i}{sorted_filenames_file_extension}'
                            with open(current_filename, 'rb') as current_file:
                                file_content = current_file.read()
                                output_file.write(file_content)
                            
                            # remove sorted files and leave incidence.log
                            os.remove(current_filename)
                    print('incidence.log created') # debugging

        # ensure index doesn't exceed 10
        i += 1
        if i == 11:
            i -= 10

if __name__ == '__main__':

    FILE_PATH = 'DATA' + os.sep
    FILENAME = 'grc_test_file_custom.bin'
    
    MAX_FILESIZE = 12.288e09

    main()

