# Notes on running the scorm.py script which produces a SCORM package

#Prerequisites
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

#Running the Python script
    You just need to provide two arguments with the python script:
    The first argument is the name you want to give your scorm package.
    The second argument is the name of your created self-contained html file (created in the Prerequisites)

#For help run -h or --help "python scorm.py -h" otherwise contact thomas.hutcheson@moneysupermarket.com
