import os
import re
import shutil

target_dir = "mods/"

if __name__ == "__main__":
    directories = os.listdir( target_dir )
    pattern = re.compile( "[0-9]+" )
    for containing_folder in directories:
        if os.path.isdir( target_dir + containing_folder ) and pattern.match( containing_folder ):
            for file in os.listdir( target_dir + containing_folder + "/" ):
                shutil.copyfile( target_dir + containing_folder + "/" +  file, target_dir + containing_folder + file )
