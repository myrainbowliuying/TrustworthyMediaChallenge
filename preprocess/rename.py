import os
import argparse

#path="E:\\TurstworthyMediaChallenge\\Audios\\Real\\wav48"
def main(config):
    subfolders=os.listdir(config.path)
    for subfolder in subfolders:
        filenames=os.listdir(os.path.join(config.path,subfolder))
        for filename in filenames:
            new_name=subfolder+'-'+filename
            dst=os.path.join(config.path,subfolder)
            dst=os.path.join(dst,new_name)
            src=os.path.join(config.path,subfolder)
            src=os.path.join(src,filename)
            os.rename(src,dst)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-i', type=str)

    config = parser.parse_args()
    main(config)
