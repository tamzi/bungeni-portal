# Bungeni Update Template #

While using the update template place latest and previous debian packages
in their respective folders  and run the first 3 commands in the order given below
or you can just run the 4th command.


1) **udoxtract.sh** - Update do extract on debian packages in the previous and latest folders


2) **udodiff.sh** - Update do diff on extracted content


3) **udogen.sh** - Do generate debian package update


4) **udobuild.sh** - Runs the above three commands in that order


5) **udoclean.sh** - Do generated content clean out


The update.ini file stores basic information about update package, the filter.words file is
used by the diff command to filter out any path that contains words in that specific path name.

Please note when the generated debian package is installed it will extract its new contents from
to **/opt/bungeni/updates** to thier destination.