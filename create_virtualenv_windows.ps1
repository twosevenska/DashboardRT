# This script was made in order to install and configure the first setup of the Virtualenv

# If you run into an error that says scripts have been disabled on your system you need to
# change your policy file. 

# First let's install the Virtualenv in a new env directory under the current folder

pip install virtualenv
virtualenv env 

# Now let's start it up, since this is a powershell script we need to start the .ps1 script 

.\env\Scripts\activate.ps1

# And now let's install all dependencies in the env, as well as the current dashboard code

pip install -e .

# Last but not least time to close the env 

deactivate

# Actually we also need to return to the previous directory

cd ..