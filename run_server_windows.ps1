# Ok, since we're all lazy this script starts a copy of the env with a fresh server build 
# and starts it up

# Since this is a powershell script we need to start the .ps1 script inside the env directory

.\env\Scripts\activate.ps1

# And now let's rebuild the server code

pip install -e .

# And let's head into the server folder so we can start it

cd .\ditic_kanban

# Finally we start the server

ditic_kanban_server
