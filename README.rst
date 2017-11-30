# RRS4suadeTest

:Info: Rough Report Exporting Service for a test


instructions::
 
install/download::
    ``git clone https://github.com/kumrzz/RRS4suadeTest``
    
    ``cd RRS4suadeTest``

run RRSserver on a separate terminal::
    ``python RRSserver.py``

run RRSclient on a separate terminal::
    ``python RRSclient.py``


not had the time to write tests, but they'd entail changing input params to RRSclient.py:

* Record : this is the record number being requested

* FileType: xml or pdf 

Further work:

* should be celery'd as doc generation can be a long process

Footnotes:

prerequisites(libraries): python-psycopg2, libxslt-dev, libxml2-dev, python-lxml, (pip)pdfkit, (pip)lxml, (pip)wkhtmltopdf

I chose lxml.etree over xml.elementtree mainly as it can do indenting and is more feature-rich.
