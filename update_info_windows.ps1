# This one is not about being lazy, just that currently it's really messed up the way this works
# So if you want to update the charts this is the thing you'll run

# Since this is a powershell script we need to start the .ps1 script inside the env directory

.\env\Scripts\activate.ps1

# And let's head into the server folder so we can start it

cd .\ditic_kanban

# Finally we run the commands
generate_summary_file
update_statistics

# And get out 

deactivate

# Actually we also need to return to the previous directory

cd ..