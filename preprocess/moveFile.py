import os,shutil
import argparse

#old_path='E:\\TurstworthyMediaChallenge\\Real\\1080p'
#new_path="E:\\TurstworthyMediaChallenge\\RealAudios\\wav48"
def main(config):
    subfolders=os.listdir(config.old_path)
    for subfolder in subfolders:
        dst=os.path.join(config.new_path,subfolder)
        if not os.path.exists(dst):
            os.makedirs(dst)
        filenames=os.listdir(os.path.join(config.old_path,subfolder))
        for filename in filenames:
            src=os.path.join(config.old_path,subfolder)
            src=os.path.join(src,filename)
            if filename[4:] == "wav":
                try:
                    shutil.move(src,dst)
                except OSError:
                    pass

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--old_path','-i',type=str)
    parser.add_argument('--new_path','-o',type=str)

    config = parser.parse_args()
    main(config)