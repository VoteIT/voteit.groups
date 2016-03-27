 #!/bin/bash
 #You need lingua and gettext installed to run this
 
 echo "Updating voteit.groups.pot"
 pot-create -d voteit.groups -o voteit/groups/locale/voteit.groups.pot .
 echo "Merging Swedish localisation"
 msgmerge --update voteit/groups/locale/sv/LC_MESSAGES/voteit.groups.po voteit/groups/locale/voteit.groups.pot
 echo "Updated locale files"
 