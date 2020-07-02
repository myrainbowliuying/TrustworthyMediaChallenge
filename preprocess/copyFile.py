import os,shutil
import argparse

def main(config):
    filenames=os.listdir(config.old_path)

    for filename in filenames:
        src=os.path.join(config.old_path,filename)
        dst=os.path.join(config.new_path,filename)
        if filename[4:] == "wav":
            try:
                shutil.copy(src,dst)
            except OSError:
                pass

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--old_path','-i',type=str)
    parser.add_argument('--new_path','-o',type=str)

    config = parser.parse_args()
    main(config)