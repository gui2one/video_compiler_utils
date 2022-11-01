import configparser
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

def replaceVersion(file_path, line_pattern, major, minor, revision):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if line_pattern in line :
                    changed_line = f'#define MyAppVersion "{major}.{minor}.{revision}"\n'
                    print(f'\t{line.strip()} -> {changed_line}')
                    new_file.write(changed_line)
                else:
                    new_file.write(line)
                # new_file.write(line.replace(pattern, subst))
    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

ENV_FILE = '.env'
config = configparser.ConfigParser()
config.read(ENV_FILE)
version_major = config["VERSION"]['VERSION_MAJOR']
version_minor = config["VERSION"]['VERSION_MINOR']
version_rev   = config["VERSION"]['VERSION_REVISION']

old_version = f'{version_major}, {version_minor}, {version_rev}' 
# bump revision number every time
config["VERSION"]['VERSION_REVISION'] = str(int(version_rev)+1)

with open(ENV_FILE, 'w') as configFile:
    config.write(configFile)
    
config.read(ENV_FILE)
version_major = config["VERSION"]['VERSION_MAJOR']
version_minor = config["VERSION"]['VERSION_MINOR']
version_rev   = config["VERSION"]['VERSION_REVISION']
new_vrersion = f'{version_major}, {version_minor}, {version_rev}'

header_file = "src/version_infos.py"
print(f"changing version in python file :{header_file}")
print(f'\t{old_version} -> {new_vrersion}')


content = f'''
VCU_VER_MAJOR = {version_major}
VCU_VER_MINOR = {version_minor}
VCU_VER_REVISION = {version_rev}
'''
with open(header_file, "w") as file:
    file.write(content)
    
    
## #change version in inno setup to
inno_setup_file = "inno_setup/setup.iss" 
print(f"changing version in : {inno_setup_file}")
replaceVersion(inno_setup_file, "#define MyAppVersion", version_major, version_minor, version_rev)