#!/usr/bin/python
import os
import sys
from distutils.dir_util import copy_tree
from jinja2 import Environment, FileSystemLoader, Template
import zipfile
import shutil
import argparse


def argumentParser():
    """
    Creates a -h / --help flag that describes what the user is required to do, sets a requirement for two arguments to run the script, 1) scorm package name and 2) the name of a html file.
    """
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-h', '--help', action='help', help='To run this script please provide two arguments: first argument should be your scorm package name, second argument should be your html file name. Note: Any current zipped folder in the run directory with the same scorm package name will be overwritten.')
    parser.add_argument('package_name', action="store",  help='Please provide your scorm package name as the first argument')
    parser.add_argument('html_file_name', action="store", help='Please provide your html file name as the second argument')

    return parser.parse_args()


def create_directories(dirName):
    """
    Create directories
    """
    # Create directory
    
    try:
        # Create target Directory
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ") 
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")        
        exit(1)
    subDirName = dirName+'/res'
    
    # Create target directory & all intermediate directories if don't exists
    try:
        os.makedirs(subDirName)    
        print("Directory " , subDirName ,  " Created ")
    except FileExistsError:
        print("Directory " , subDirName ,  " already exists")  
    return subDirName


def copy_files(dirName, static):
    """
    Copy xsd files from static folder to named directory
    """
    
    fromDirectory = static
    toDirectory = dirName
    try:
      copy_tree(fromDirectory, toDirectory)
      print("Content Copied From " , fromDirectory ,"to", toDirectory,  " Successfully ") 
    except FileExistsError:
      print("Content Failed to Copy From " , fromDirectory ,"to", toDirectory,  "")  
      exit(1)
      

def copy_resources(subDirName, resfiles):
    """
    Copy resource files from resource folder to named directory sub folder res
    """
    
    fromDirectory = resfiles
    toDirectory = subDirName
    try:
      copy_tree(fromDirectory, toDirectory)
      print("Content Copied From " , fromDirectory ,"to", toDirectory,  " Successfully ") 
    except FileExistsError:
      print("Content Failed to Copy From " , fromDirectory ,"to", toDirectory,  "")  
      exit(1)

def resourcelist(resource_content):
    """
    Gets all the file paths for the content of the newly created sub-directory "/res"
     which is used in jinj_template which edits the imsmanifest.xml file.
    """
    all_resources = os.listdir (resource_content)
    output = ["res/" + f for f in all_resources ]
    return output

def jinja_template(dirName, htmlfile, all_resources, templatefile): 
    """
    Edits the imsmanifest.xml file, adds a list of the resource files to the xml.
    """

    f = open(templatefile)
    
    mytext = f.read()
    template = Template(mytext)
    
    output = template.render(starting_resource = htmlfile, resourcelist =  all_resources, title=dirName)
    
    outfile = open(dirName +'/imsmanifest.xml', 'w')
    outfile.write(output)
    outfile.close()

#----------------------------
#Zip folder to create scorm package
#------------------------------

def retrieve_file_paths(dirName):
    """ 
    Retrieves the filepath for the directoy being zipped. 
    """
    # setup file paths variable
    filePaths = []
    
    # Read all directory, subdirectories and file lists
    for root, directories, files in os.walk(dirName):
      for filename in files:
          # Create the full filepath by using os module.
          filePath = os.path.join(root, filename)
          filePaths.append(filePath)
          
    # return all paths
    return filePaths
 

def zip_directory(dirName):
    """ 
    The zip_directory function zips the content of the created score_package folder. 
    """
    
  # Assign the name of the directory to zip
    dir_name = dirName
    
    # Call the function to retrieve all files and folders of the assigned directory

    filePaths = retrieve_file_paths(dir_name)
      
    # printing the list of all files to be zipped
    print('The following list of files will be zipped:')
    for fileName in filePaths:
      print(fileName)
        
    # writing files to a zipfile
    zip_file = zipfile.ZipFile(dir_name+'.zip', 'w')
    with zip_file:
      # writing each file one by one
      for file in filePaths:
        zip_file.write(file)
          
      print(dir_name+'.zip file is created successfully!')

    
def delete_directory(dirName):
    """ 
    The delete_directory function deletes the created folder structure leaving the user with just the zipped scorm package.
    """     
    
    # delete directory
    dirName = dirName
    
    try:
        # Delete target Directory
        shutil.rmtree(dirName, ignore_errors=False, onerror=None)
        print("Directory " , dirName ,  " Deleted ") 
    except FileExistsError:
        print("Directory " , dirName ,  " Failed to Delete")        


def main():
    
    args = argumentParser()
    dirName=args.package_name
    htmlResource=args.html_file_name

    subDirName = create_directories(dirName)

    resource_content = dirName + '/res/'
    
    copy_files(dirName = dirName, static ='static/')
    
    copy_resources(subDirName = subDirName, resfiles = 'resources/')

    resources = resourcelist(resource_content)
   
    jinja_template(dirName = dirName, htmlfile = 'res/' + htmlResource, 
                all_resources =resources,
                templatefile = "static/imsmanifest.xml")

    zip_directory(dirName = dirName)
    
    delete_directory(dirName = dirName)   
    
# Call the main function
if __name__ == "__main__":
  main()