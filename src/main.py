import shutil
import os
from gencontent import generate_pages_recursive
import sys

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def clean_public_folder():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
        
def static_to_public():
    copy_file(dir_path_static,dir_path_public)
    
def copy_file(src,dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    for item in os.listdir(src):
        src_item = os.path.join(src,item)
        dest_item = os.path.join(dest,item)
        if os.path.isfile(src_item):
            shutil.copy(src_item,dest_item)
        else:
            copy_file(src_item,dest_item)


def main():
    args = sys.argv
    basepath = "/"
    if len(args) ==2:
        basepath = args[1]
    print("Deleting public directory...")
    clean_public_folder()
    print("Copying static files to public directory...")
    static_to_public()
    print("Generating page...")
    print("Generating content...")
    generate_pages_recursive(basepath,dir_path_content, template_path, dir_path_public)

        
if __name__ == "__main__":
    main()
    

