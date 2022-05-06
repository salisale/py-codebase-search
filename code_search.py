import os
import sys

# please narrow down your search folders as to not include junk/irrelevant files
# e.g. /frontend/node_modules/*
module_dir = 'C:/Users/s.lohavittayavikant/dev/TMS/classic/ls-web/src'
module_dir_main = module_dir + '/main/java'
module_dir_test = module_dir + '/test/java'
search_targets = [module_dir_main, module_dir_test]

if len(sys.argv) < 2:
    print('Error: argument missing')
    print('Please specify the target text to search e.g. ')
    print('$ python [SCRIPT_NAME.py] DHLWEB.ServiceURL.GLS || com.dhl.phx_dc.scxgxtt.euexpressratebook')
    exit(1)

target_str = sys.argv[1]

# get all files
all_files = []
for target in search_targets:
    for folder, subfolders, files in os.walk(target):
        for file in files:
            # get only .java files or Test files (no extension)
            # becareful of noextension file =>
            if file.split(".")[-1] == 'java' or file.split(".")[-1] == file:
                filePath = os.path.join(folder,file).replace("\\","/")
                all_files.append(filePath)

print('----------')
print('searching in ' + str(len(all_files)) + ' files for ' + target_str)
print('----------')

out_dict = {}
for file in all_files:
    with open(file, 'r') as inF:
        lines = inF.read().splitlines()
        for line in lines:
            if target_str in line:
                out_dict[file] = out_dict.get(file,0) + 1

# convert dict to tuple, sort by count
out_tuples = sorted(list(out_dict.items()),key=lambda x: x[1], reverse=True)
out_main_files = [tup for tup in out_tuples if 'main' in tup[0]]
out_test_files = [tup for tup in out_tuples if 'test' in tup[0]]

# print result
if len(out_main_files) > 0:
    print('\n## Main ##')
    for tuple in out_main_files:
        print(tuple[0].replace(module_dir, '..') + ' [ %d ]' %tuple[1])
if len(out_test_files) > 0:
    print('\n## Test ##')
    for tuple in out_test_files:
        print(tuple[0].replace(module_dir, '..') + ' [ %d ]' %tuple[1])
