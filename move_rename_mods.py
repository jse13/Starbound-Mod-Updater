import os
import re
import shutil

if __name__ == "__main__":
    directories = os.listdir( "." )
    pattern = re.compile( "[0-9]+" )
    for i in directories:
        if os.path.isdir( i ) and pattern.match( i ):
            for j in os.listdir( i + "/" ):
                shutil.copyfile( i + "/" + j, i + j )
                print( "Moving file " + j )
