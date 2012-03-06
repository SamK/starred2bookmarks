#!/bin/sh
SOURCE=site
DEST=/var/www/uiop.ch/starred2bookmarks
/bin/cp  -r $SOURCE/model.py  $SOURCE/model.pyc  $SOURCE/site.py  $SOURCE/static  $SOURCE/templates  $SOURCE/web $DEST
mkdir -p $DEST/var
chmod 777 $DEST/var

