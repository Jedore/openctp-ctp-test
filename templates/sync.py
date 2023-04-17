"""
    Sync pyproject.toml/__about__.py/init.py
    Execute this module in project root directory.
"""

import os
import shutil
import sys

if __name__ == '__main__':
    try:
        ctp_version = sys.argv[1]
    except IndexError:
        print('Execute in project root directory: \n'
              '     python sync.py <ctp version>')
        exit(-1)

    target_dir = os.path.join(os.getcwd(), f'openctp-ctp-{ctp_version}')
    print('Target dir', target_dir)

    print('Sync __about__.py')
    with open(os.path.join('templates', '__about__.py'), 'r') as file_obj:
        text = file_obj.read()
    new_text = text.replace('PKG_VERSION', '3.0.3')
    with open(os.path.join(target_dir, 'libs', '__about__.py'), 'w') as file_obj:
        file_obj.write(new_text)

    print('Sync __init__.py')
    shutil.copyfile(os.path.join('templates', 'init.py'), os.path.join(target_dir, 'libs', '__init__.py'))

    print('Sync pyproject.toml')
    with open(os.path.join('templates', 'pyproject.toml'), 'r') as file_obj:
        text = file_obj.read()
    version = f'{ctp_version[0]}.{ctp_version[1]}.{ctp_version[2:]}'
    new_text = text.replace('CTP_VERSION2', version)
    new_text = new_text.replace('CTP_VERSION', ctp_version)
    with open(os.path.join(target_dir, 'pyproject.toml'), 'w') as file_obj:
        file_obj.write(new_text)

    print('Sync README.md')
    with open(os.path.join('templates', 'README.md'), 'r') as file_obj:
        text = file_obj.read()
    new_text = text.replace('CTP_VERSION', ctp_version)
    with open(os.path.join(target_dir, 'README.md'), 'w') as file_obj:
        file_obj.write(new_text)

    print('Sync hook')
    with open(os.path.join('templates', 'hatch_build_hook.py'), 'r') as file_obj:
        text = file_obj.read()
    new_text = text.replace('CTP_VERSION', ctp_version)
    with open(os.path.join(target_dir, 'hatch_build_hook.py'), 'w') as file_obj:
        file_obj.write(new_text)
