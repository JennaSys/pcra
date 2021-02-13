import subprocess
import sys

from pcra import __version__


VERSION_FILE = 'pcra/__init__.py'

levels = dict(major=0, minor=1, patch=2)


def get_new_version(level=None):
    ver = [int(ver) for ver in __version__.split('.')]

    if level is not None:
        for lev_num in range(level, 3):
            if lev_num == level:
                ver[lev_num] += 1
            else:
                ver[lev_num] = 0

    return '.'.join([str(ver_num) for ver_num in ver])


def tag_git(ver):
    clean = subprocess.check_output(['git', 'status', '--porcelain']) == b''

    if clean:
        update_local(ver)
        subprocess.check_output(['git', 'add', VERSION_FILE])
        subprocess.check_output(['git', 'commit', '-m', f'Version {ver}'])
        subprocess.check_output(['git', 'tag', f'v{ver}'])
        return True
    else:
        print(f"ERROR: Git repository is not clean!  Commit changes and try again")
        return False


def update_local(ver):
    with open(VERSION_FILE, 'w') as version_file:
        version_file.write(f'__version__ = "{ver}"\n')


def main():
    if len(sys.argv) > 1:
        lev = sys.argv[1]
        if lev in levels:
            new_ver = get_new_version(levels[lev])

            if tag_git(new_ver):
                print(f'Version updated to {new_ver}')
        else:
            print(f"ERROR: '{lev}' is not a valid semver level!")
    else:
        cur_ver = get_new_version()
        print(f'Version is currently at {cur_ver}')


if __name__ == '__main__':
    main()
