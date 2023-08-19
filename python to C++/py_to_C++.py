import os
import shutil
import subprocess

def list_files_with_extension(directory, extension):
    return [file for file in os.listdir(directory) if file.endswith(extension)]

def select_file(files, prompt_message):
    print(prompt_message)
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")
    choice = int(input("Please enter the number of your choice: ")) - 1
    return files[choice]

def process_script(source_file, target_file, icon_file):
    try:
        with open(source_file, "r", encoding="utf-8") as source:
            content = source.read()
    except FileNotFoundError:
        content = ""
    
    if 'import sys' not in content:
        content = 'import sys\nimport os\n\n' + content
        with open(target_file, "w", encoding="utf-8") as target:
            target.write(content)
            print(f"Created and modified {target_file}")

    packaging_command = f'nuitka --windows-icon-from-ico={icon_file} {target_file}'
    subprocess.run(packaging_command, shell=True, check=True)
    print(f"Packaged {target_file} into an executable using Nuitka.")

def delete_folder_or_file(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Deleted {path}")
        else:
            os.remove(path)
            print(f"Deleted {path}")

def main():
    current_directory = "."
    py_file_list = list_files_with_extension(current_directory, ".py")
    ico_file_list = list_files_with_extension(current_directory, ".ico")

    selected_py_file = select_file(py_file_list, "Please select the Python script to package:")
    selected_ico_file = select_file(ico_file_list, "Please select an icon file:")

    target_script_file = os.path.join(os.path.dirname(selected_py_file), os.path.basename(selected_py_file).replace(".py", "-to-c++.py"))
    shutil.copy(selected_py_file, target_script_file)
    process_script(target_script_file, target_script_file, selected_ico_file)

    build_folder = os.path.splitext(target_script_file)[0] + ".build"
    cmd_file = f"{os.path.splitext(target_script_file)[0]}.cmd"

    delete_all = input("Do you want to delete the generated .build folder and .cmd file? (y/n): ")
    if delete_all.lower() == "y":
        delete_folder_or_file(build_folder)
        delete_folder_or_file(cmd_file)

    generated_exe_file = os.path.splitext(target_script_file)[0] + ".exe"
    renamed_exe_file = generated_exe_file.replace("-to-c++", "")
    os.rename(generated_exe_file, renamed_exe_file)
    print(f"Renamed {generated_exe_file} to {renamed_exe_file}")

if __name__ == "__main__":
    main()
