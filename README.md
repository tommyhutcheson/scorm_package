# Notes on producing slides for SCORM package

Create markdown file with slide source (test.md in this example).

Folder structure

/source/test.md
/source/images/<image files to include>

Use pandoc to compile self-contained HTML slides with the slidy framework (requires connection to web to get slidy CSS). 

https://pandoc.org/MANUAL.html#producing-slide-shows-with-pandoc

## Create HTML slides:
pandoc -t slidy --self-contained test.md -o test.html

(can also create PDF slides - requires pdfLaTeX)
pandoc -t beamer test.md -V theme:Warsaw -o test.pdf


## Create a SCORM package

Course_1.zip is a valid scorm package.
File `imsmanifest.xml` is the definition of what goes in the package.  The other XSD files are required boilerplate that we don't need to fiddle with.
Folder `Course_1/res/` is where we put the slides and any other files that are needed (in this example a PDF file).

Around line 28-32 there is a resource tag that defines what files are in the package and which one should be the start when the learning management system (LMS) launches the package (our LMS is Looop but there are plenty of others on the market).

```xml
<resource identifier="resource" type="webcontent" adlcp:scormtype="sco" href="res/test.html">
<file href="res/test.html"/>
<file href="res/GitCoreConcepts.pdf"/>
</resource>
```

Wrapping the contents of the Course_1 folder up as a zip (as it is in the folder here) is what produces a scorm package. 

# Steps to script things up

## Set up a template scorm folder
this contains all the boilerplate XSDs and templates etc

## copy boilerplate into a tmp folder

## Use Jinja2 template for imsmanifest
We can use a Jinja2 template to make the resource file list and starting resource into variables
e.g. something like:
 
```xml
<resource identifier="resource" type="webcontent" adlcp:scormtype="sco" href="{{starting_resource}}">
{% for resource in resourcelist %}
            <file {{ resource }} >
{% endfor %}
</resource>
``` 

## create imsmanifest from list of files the user provides and put that in tmp folder
## copy user's input files into `/res/` in the tmp folder
## zip up the tmp folder to produce a scorm package.


# scorm_package
