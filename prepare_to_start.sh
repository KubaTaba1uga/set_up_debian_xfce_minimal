#!/bin/bash
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# Install and configure sudo if, not installed
if ! [ -x "$(command -v sudo)" ]; then
	echo "root authentication"
	su - root  -c "/bin/bash $SCRIPT_DIR/.prep/set_up_sudo.sh"
fi

PYTHON_VERSION=`python3 -V | cut -d "." -f 2`

# If python version is smaller than 3.9
#   install python 3.9.8
if [ $PYTHON_VERSION -lt 9 ]; then
        /bin/bash $SCRIPT_DIR/.prep/install_python3_9.sh
fi

# Install app dependencies
/bin/bash $SCRIPT_DIR/.prep/install_dependencies.sh
