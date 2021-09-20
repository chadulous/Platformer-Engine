import os
def increment_ver(ver):
    print(ver)
    ver = ver.split('.')
    print(ver)
    ver[2] = str(int(ver[2]) + 1)
    return '.'.join(ver)
version = open('.ver', 'r+')
vernum = version.read()
newver = increment_ver(vernum)
os.system(f'powershell .\\build.ps1 {newver}')
version.write(newver)
version.close()