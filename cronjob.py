from os import environ
from subprocess import check_output
from subprocess import CalledProcessError
from subprocess import call
from imp import load_source
updater = load_source("starbound_update", environ.get( "HOME" ) + "/Starbound-Mod-Updater/starbound_update.py")

def get_pid_by_name( name ):
    try:
        process_pid = check_output([ "pidof", name ] )[0:-1]
    except CalledProcessError:
        process_pid = "INVALID"
    return process_pid

def interrupt_process( pid ):
    try:
        call( "kill -s INT " + pid, shell=True )
        return True;
    except CalledProcessError:
        return False;


if __name__ == "__main__":

    # Kill server if it is currently running
    server_pid = get_pid_by_name( "starbound_server" )
    if( server_pid == "INVALID" ):
        # TODO: log to file
        print "Server is not running"
    else:
        if( not interrupt_process( server_pid ) ):
            # TODO: log that server could not be killed
            exit();
    
    # Run the update script
    updater.main()

    # Start the server up again

