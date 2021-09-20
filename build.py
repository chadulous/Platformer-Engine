import os
def increment_ver(ver):
    print(ver)
    ver = ver.removeprefix('v').split('.')
    print(ver)
    ver[2] = str(int(ver[2]) + 1)
    if int(ver[2]) >= 10:
        ver[2] = str(0)
        ver[1] = str(int(ver[1]) + 1)
    if int(ver[1]) >= 10:
        ver[1] = str(0)
        ver[0] = str(int(ver[1]) + 1)
    return 'v' + '.'.join(ver)
version = open('.ver', 'r')
vernum = version.read()
newver = increment_ver(vernum)
version.close()
os.system(f'powershell .\\build.ps1 {newver}')
version = open('.ver', 'w')
version.write(newver)
version.close()