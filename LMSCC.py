import subprocess
import os
import zipfile
import argparse

def TryCompile(src):
    result = False
    output_file = src[0].split('.')[0]

    gcc_command = ['gcc', *src, '-o', output_file]
    try:
        r = subprocess.run(gcc_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = True
    except subprocess.CalledProcessError as e:
        result = False
    return result
        

def extract_zip_recursively(zip_path, extract_to):
    if not os.path.exists(zip_path):
        print(f"Error: {zip_path} does not exist.")
        return

    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        
        for file in os.listdir(extract_to):
            file_path = os.path.join(extract_to, file)
            if zipfile.is_zipfile(file_path):
                new_extract_to = os.path.join(extract_to, os.path.splitext(file)[0])
                extract_zip_recursively(file_path, new_extract_to)
                

def list_directories(path):
    return [path + '/' + item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]

def find_files(root_folder, targetfiles):
    matches = []
    for root, dirs, files in os.walk(root_folder):
        for targetfile in targetfiles:
            if targetfile in files:
                matches.append(os.path.join(root, targetfile))
    return matches
    
def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('input_zip', type=str, help="Input file path")
    parser.add_argument('grade_subjects', type=str, nargs='+', help="C-sources to grade")
    args = parser.parse_args()
    
    srcs = args.grade_subjects
    print('# TARGET SOURCECODEs')
    for i in range(0, len(srcs)):
        srcs[i] = srcs[i].split(',')
        print(srcs[i])

    zip_file_path = args.input_zip
    extract_to = zip_file_path.split('.')[0]
    extract_zip_recursively(zip_file_path, extract_to)
    reports = list_directories(extract_to)
    for report in reports:
        issues = []
        for src in srcs:
            target_lab = find_files(report, src)
            if len(target_lab) == 0:
                issues.append('     #No such reports(' + src[0] + ').')
                continue
            if TryCompile(target_lab) == False:
                issues.append('     #An error has occurred while compiling (' + src[0] + ').')
                continue
        if len(issues):
            print(report + ' =>')
            for issue in issues:
                print(issue)
    
if __name__ == "__main__":
    main()