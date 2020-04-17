import subprocess
import glob, os


def syscall(arg):
    PATH_KDFF = os.path.abspath(os.path.dirname(__file__))+ '/vendor/kdff/kdff.exe'
    subprocess.call(PATH_KDFF+arg)

def main():
    dffPath= "D:/jmmaps/vcs2samp/vcsimg"
    os.chdir(dffPath)

    for filename in glob.glob("*.dff"):
        filename = os.path.splitext(filename)[0]
        filename = dffPath +"/" + filename

        arg = " -a -d \"{}.dff\" -c \"{}.col\" -o \"{}.dff\"".format(filename,filename,filename)
        syscall(arg)
        print("process:{}".format(arg))
    print()

main()