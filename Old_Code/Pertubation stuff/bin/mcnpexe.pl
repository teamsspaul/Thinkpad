#!/usr/bin/perl

###############################################################################
#                                                                             #
# mcnpexe - script to load & execute the proper verion of MCNP on the LANL    #
#           hpc clusters.                                                     #
#                                                                             #
# NOTES:                                                                      #
# (1) Any special options for this script must occur BEFORE the mcnpexe       #
# arguments. They are discarded and not passed to mcnp.                       #
#                                                                             #
###############################################################################

use Socket;

use Env;
use Sys::Hostname;
use Time::HiRes;
use warnings;
use POSIX qw(strftime);

##########################################################
# Check for proper unix group before we do anything else #
##########################################################
validate_user("mcnp");

#############################
# Set some global variables #
#############################
my $DEBUG          = 0;
my $PRINTRUNINFO   = 1; # on by default #
my $INP            = 'inp';
my $HAVE_INP       = 'yes';
my $PLOTTING       = 'no';
my $BLEEDINGEDGE   = 'no';
my $EOL            = '';
my $CLUSTER        = '';
my $shell          = '/bin/sh';
my $UNLIMIT        = 'ulimit -s unlimited';

my $EOLUS_DIR      = '';
my $MCNP           = '';
my $MCNP5          = '';
my $MCNP5MPI       = '';
my $MCNP6          = '';
my $MCNPBE         = '';
my $MCNPBEMPI      = '';
my $MPIBEHOST      = '';
my $MCNPCMDLINE    = '';
my $MCNPMPI        = '';
my $MCNPMPICMDLINE = '';
my $MPI            = 'no';
my $PRUN           = '';
my $NP             = '';
my $OSVER          = '';
my $LISTEXECS      = 0;

#########################################
# For computing elapsed wall clock time #
#########################################
my ($start, $end, $elapsed);

###################
# Get the OS name #
###################
chomp ($OS = `uname`);
my $HOST = hostname;

####################################################
# Set the projects directory and other values that #
# depend on which system (HPC or XLan) we are on   #
####################################################
if ( $OS eq 'Linux' ) {
    if (($HOST =~ "ml|mp|wf|mu")) { # moonlight, mapache, wolf, mustang
	require "$ENV{'MODULESHOME'}/init/perl";
	$MODULES = "intel/15.0.5 openmpi/1.6.3 totalview";
    }
    elsif ($HOST =~ "barugon|xr|varan|firehouse") { # XLan systems
	require "$ENV{'MODULESHOME'}/init/perl.pm";
	$MODULES = "intel/15.0.5 openmpi/1.6.3";
    }
}
&module("purge");

###############
# Linux Setup #
###############
require lib;
if ( $OS eq 'Linux' ) {
    if ($HOST =~ "barugon|xr|varan|firehouse") { # XLan systems
        print "HOST is $HOST\n" if ($DEBUG);
        if ($HOST =~ "barugon") {
	    $MPIBEHOST = "ba";
	} elsif ($HOST =~ "varan") {
	    $MPIBEHOST = "va";
	}  # don't build for other hosts on xlan
        $MCNP6     = "mcnp6_rel_6-1-1beta_2014-07-16";
        $MCNP6MPI  = "mcnp6_lanl_1.0.mpi";
        #$MCNP6MPI  = "mcnp6_11.mpi";
        $HOST      = "XLan";
        $HOSTCODE  = "xlan";
	$MCNP5     = "mcnp5_rsicc_1.60_linux_x86_64_omp";
	$MCNP5MPI  = "";  #"mcnp5_lanl_1.60.mpi";
	$EOLUS_DIR = "/opt/local/codes/mcnp/bin";
	lib->import( "/opt/local/codes/mcnp/bin" );
	require PRINT_run_info;
	if (!$ENV{'DATAPATH'}) {
	    $ENV{'DATAPATH'} = '/opt/local/codes/mcnp/MCNP_DATA';
	} 
    } elsif (($HOST =~ "ml|mp|wf|mu")) { # moonlight, mapache, wolf, mustang
	print "HOST is $HOST\n" if ($DEBUG);
	$MCNP5     = "mcnp5_lanl_1.60";
	$MCNP5MPI  = "mcnp5_lanl_1.60.mpi";
	$MCNP6     = "mcnp6_rel_6-1-1beta_2014-07-16";
	#$MCNP6     = "mcnp6_lanl_1.0.omp";
        $MCNP6MPI  = "mcnp611.mpi";
	$EOLUS_DIR = "/usr/projects/mcnp";
	lib->import( "/usr/projects/mcnp/TOOLS/EOLUSBIN" );
	require PRINT_run_info;
	if (!$ENV{'DATAPATH'}) {
	    $ENV{'DATAPATH'} = '/usr/projects/mcnp/MCNP_DATA';
	}
        # specific host dependant values #
	if ($HOST =~ "ml")  {
	    $MCNP6MPI  = "mcnp611.mpi"; 
	    $HOST      = "moonlight";
	    $HOSTCODE  = "ml";
	    # print "Please llogin first....\n";
	    # exit;
	} elsif ( $HOST =~ "mp" ) { 
	    $MCNP6MPI  = "mcnp611.mpi";
	    $HOST      = "mapache";
	    $HOSTCODE  = "mp";
	    # print "Please llogin first....\n";
	    # exit;
	} elsif ( $HOST =~ "wf" ) { # wolf #
	    $MCNP6MPI  = "mcnp611.mpi";
	    $HOST      = "wolf";
	    $HOSTCODE  = "wf";
	    # print "Please llogin first....\n";
	    # exit;
	} elsif ( $HOST =~ "mu" ) { # mustang #
	    $MCNP6MPI  = "mcnp611.mpi";
	    $HOST      = "mustang";
	    $HOSTCODE  = "mu";
	    # print "Please llogin first....\n";
	    # exit;
	} 
	$MPIBEHOST = $HOSTCODE;
    # add new file systems here: elsif ( $HOST =~ "<name>") {....}
    } else {
	print "Linux machine $HOST is not supported by the MCNP team\n";
	$PRINTRUNINFO = 0;
	print "****************************************************************\n";
	print "****************************************************************\n";
	print " File system not recognized - \n";
	print "               this machine is not supported by this script\n";
	print " Results are unpredictable.\n";
	print "****************************************************************\n";
	print "****************************************************************\n";
	exit;
    }
    $MCNPBE    = "MCNP6_BE.omp";
    $MCNPBEMPI = "MCNP6_BE_" . $MPIBEHOST . ".mpi";
    print "MCNPBEMPI is $MCNPBEMPI\n";
} else { # unsupported OS
    $PRINTRUNINFO = 0;
    print "OS $OS is not supported by this script\n";
    exit;
}

open(STDERR, ">&STDOUT"); 

my $MCNPVERSION = "not-found"; # for sweeper reporting #

##############################
# Save the command-line args #
##############################
@USR_ARGS = @ARGV;

###############################################################
# Scan the command-line args for script options & remove them #
###############################################################
my $arg;
while ( $arg = shift @USR_ARGS ) 
{
    if (($arg eq '-debug')   || 
	($arg eq '-verbose')   )
    {
        $DEBUG = 1; 
    }
    elsif ($arg eq '-execlist') {
	# List all of the executables that are available
        $LISTEXEC = 1;
    }
    elsif (($arg eq '-mcnp')  || 
	   ($arg eq '-mcnp5') || 
	   ($arg eq '-mcnp6') || 
	   ($arg eq '-exec')    ) 
    {
        $MCNPCMDLINE    = shift @USR_ARGS;
        $MCNPMPICMDLINE = $MCNPCMDLINE;
    }
    elsif (($arg eq '-help')  || 
	   ($arg eq '--help') ||  
	   ($arg eq '-h')     || 
	   ($arg eq '--h')    ||
	   ($arg eq '-man')     ) 
    {
        &man;
        exit;
    }
    elsif ($arg eq '-np') 
    {
        $MPI = 'yes';
        $NP  = shift @USR_ARGS;
        if ($NP eq 2) {
	    print "**** np must be 1, or greater than 2 - setting to 3 ****\n";
	    $NP = 3;
	}
    }
    elsif ($arg eq '--') 
    { 
        last; 
    }
    elsif ($arg eq '-be')
    {
        $BLEEDINGEDGE = 'yes';
        $MCNPVERSION = "MCNP6_DEVEL_2";
    }
    elsif ($arg eq '-6')
    {
        $MCNP    = $MCNP6;
        $MCNPMPI = $MCNP6MPI;
        $MCNPVERSION = "MCNP6_V6.1.1beta";
    }
    elsif ($arg eq '-5')
    {
        $MCNP    = $MCNP5;
        $MCNPMPI = $MCNP5MPI;
        $MCNPVERSION = "MCNP5_V1.6.0";
    }
    else 
    { 
        unshift @USR_ARGS, $arg; 
        last; 
    }
}

########################################################
# Read the MCNP arguments and look for important stuff #
########################################################
foreach $arg (@USR_ARGS) {
    print "arg is $arg\n" if ($DEBUG);
    ################################################
    # Check for cases when no input file is needed #
    ################################################
    if ($arg eq 'z') 
    {
        $HAVE_INP = 'no';
        last;
    }
    else 
    {
        #############################################################
        # Retreive the name of the INP file from the mcnp arguments #
        #############################################################
        if  ($arg =~ /^i[np]*=(.*)$/i)    
        { 
            $INP = $1; 
            last; 
        }
        elsif ($arg =~ /^n[ame]*=(.*)$/i) 
        { 
            $INP = $1; 
            last; 
        }
    }
    
    ######################
    # Check for plotting #
    ###################### 
    if ($arg =~ /^[ipxrz]*$/) 
    { 
        if ($arg =~ /p/) 
        { 
            $PLOTTING = 'yes';
        }
    }
}

#################################################
# Retrieve the number of threads from mcnp args #
#################################################
$TASKS="1";
for ($k = 0; $k < @USR_ARGS; $k++)
{
    if ($USR_ARGS[$k] =~ /^tasks$/i)
    {
        $t = $USR_ARGS[$k+1];
        if ($t =~ /-?\d+x(\d+)/i) 
        { 
            $TASKS = $1; 
            $OMP   = "yes";
        }
        elsif ($t =~ /(\d+)/) 
        { 
            $TASKS = $1; 
            $OMP   = "yes";
        }
        last; 
    }
}

###############
# Linux Setup #
###############
if ( $OS eq 'Linux' ) 
{
    ###########################
    # moonlight: Stable Setup #
    ###########################
    if ($HOST =~ /moonlight/ or $HOST =~ /wolf/ or $HOST =~ /mustang/) 
    {
        $CLUSTER     = "Moonlight";   # needed to get right subdirectory for stable 5 & 6
        $PLATFORM    = "moonlight";
        $MODULESHOME = "/usr/share/Modules";
        $OSVER = ''; 
        
        if ($NP eq 'all') 
        {
            $NUM_NODES = `wc -l $ENV{'PBS_NODEFILE'}`; 
            $NUM_NODES = $NUM_NODES/2;
            $TASKS     = 2;
            push @USR_ARGS, "tasks $TASKS"; 
            $OMP       = "yes";
            $NP        = $NUM_NODES;
        }
	$PRUN      = "mpirun -x TMPDIR --mca mpi_paffinity_alone 0 --bynode -np $NP";
        
    } # end moonlight
    
    #########################
    # MAPACHE: Stable Setup #
    #########################
    if ($HOST =~ /mapache/) 
    {
        print " Host is $HOST\n" if ($DEBUG);
        
        $CLUSTER     = "Mapache";   # needed to get right subdirectory for stable 5 & 6
        $PLATFORM    = "mapache";
        $MODULESHOME = "/usr/share/Modules";
        
        $OSVER = ''; 
        
        if ($NP eq 'all') 
        {
            $NUM_NODES = $ENV{SLURM_JOB_NUM_NODES} * $ENV{SLURM_CPUS_ON_NODE};
            $NUM_NODES = $NUM_NODES/2;
            $TASKS     = 2;
            push @USR_ARGS, "tasks $TASKS"; 
            $OMP       = "yes";
            $NP        = $NUM_NODES;
        }
	$PRUN = "mpirun -x TMPDIR --mca mpi_paffinity_alone 0 --bynode -np $NP";

    } # end Mapache
# what about wolf?
    ######################
    # XLan: Stable Setup #
    ######################
    if ($HOST =~ /XLan/) {
        $CLUSTER     = "";
        $PLATFORM    = "xlan";
	$MODULESHOME = "/opt/local/packages/Modules/3.2.10";
        $MODULES     = "intel/15.0.3 openmpi/1.6.3";
        $OSVER = ''; 
        
        if ($NP eq 'all') {
	    $NP = 1; #??????
	}
    }

}
else 
{
    print "OS $OS is not supported by the MCNP team\n";
    exit;
}

# if the user just wants to see which executables are available
# print them out and quit.
my $execdir    = "$EOLUS_DIR/$OS$OSVER/$CLUSTER/";
my $be_execdir = "$EOLUS_DIR/$OS/" . "BleedingEdge/";
if ($LISTEXEC) {
    # figure out which bleeding edge executables are being used
    my $be_mcnp = get_exec_name( $be_execdir, $MCNPBE);
    my $be_mcnp_mpi = get_exec_name( $be_execdir, $MCNPBEMPI);

    print "***********************************************************\n";
    print "Stable version directory: $execdir\n";
    print "Available executables:\n";
    print "     mcnp5    : $MCNP5\n";
    print "     mcnp5 mpi: $MCNP5MPI\n";
    print "     mcnp6    : $MCNP6\n";
    print "     mcnp6 mpi: $MCNP6MPI\n";
    print "Bleeding edge directory: $be_execdir\n";
    print "Available executables:\n";
    print "     mcnp6    : $be_mcnp\n";
    print "     mcnp6 mpi: $be_mcnp_mpi\n";
    print "***********************************************************\n";
    exit;
}

if ($BLEEDINGEDGE eq 'no')
{
    ##################################
    # Use one of the stable versions #
    ##################################
    if ($MCNPCMDLINE) 
    {
        $MCNP    = $MCNPCMDLINE;
        $MCNPMPI = $MCNPMPICMDLINE;
    }
    else 
    {
        $MCNP    = "$EOLUS_DIR/$OS$OSVER/$CLUSTER/$MCNP";
        $MCNPMPI = "$EOLUS_DIR/$OS$OSVER/$CLUSTER/$MCNPMPI";
    }
    
    if ($MPI eq 'yes') 
    {
        $MCNP = $MCNPMPI;
    }
}
else
{
    #########################################
    # Use the current bleeding edge version #
    #########################################
    if ($MPI eq 'yes')
    {
        $MCNP = "$be_execdir/$MCNPBEMPI";
    }
    else
    {
        $MCNP = "$be_execdir/$MCNPBE";
    }
}

#####################################
# Check for bleeding edge conflicts #
#####################################
if ($BLEEDINGEDGE eq 'yes') 
{
    $MCNPVERSION = "MCNP6_DEVEL_2";
    if ($MCNPCMDLINE ne '')
    {
        print   "\n\n";
        print   " ************************************************************\n";
        print   " * Conflicting script arguments with bleeding edge request. *\n";
        print   " * Ignoring user specified exeuctable:                      *\n";
        print   " * $MCNPCMDLINE \n";
        print   " * Using latest MCNP6 developmental version.                *\n";
        print   " ************************************************************\n\n";
    }
    
    if ($MCNP eq $MCNP6)
    {
        print   "\n\n";
        print   " ************************************************************\n";
        print   " * Conflicting script arguments with bleeding edge request. *\n";
        print   " * Ignoring user request for stable version of MCNP6        *\n";
        print   " ************************************************************\n\n";
    }

    if ($MCNP eq $MCNP5)
    {
        print   "\n\n";
        print   " ************************************************************\n";
        print   " * Conflicting script arguments with bleeding edge request. *\n";
        print   " * Ignoring user request for stable version of MCNP5        *\n";
        print   " ************************************************************\n\n";
    }
}
else
{
    if (($MCNPCMDLINE eq '') && ($MCNP eq '') && ($MCNPMPI eq ''))
    {
        print   "\n\n";
        print   " ************************************************************\n";
        print   " * Code version not specified. See script help for options. *\n";
        print   " ************************************************************\n\n";
        exit;
    }
}

my $reqTASKS = $TASKS;
my $reqNP    = $NP;

###############################
# Print the setup information #
###############################
print   "\n\n";
print   " *********************************************************\n";
print   " *********************************************************\n";
print   " \n";
print   " MCNP code             = $MCNP\n";
if ( -l $MCNP ) 
{
    my $mcnp_linktarget = readlink($MCNP);
    print " MCNP code link target = $mcnp_linktarget\n";
}

print   " \n";
print   " Host System           = $HOST\n";
print   " Operating System      = $OS$OSVER\n";
print   " Use MPI version?      = $MPI\n";
print   " Modules               = $MODULES\n";
print   " INP file              = $INP\n";
print   " \n";
print   " *********************************************************\n";
print   " *********************************************************\n";
print   " \n\n";

if ($DEBUG) 
{ 
    print " EOLUS-DIR             = $EOLUS_DIR\n"; 
    print " USR-ARGS              = @USR_ARGS\n";
    print " PLOTTING              = $PLOTTING\n";
}

#######################
# Set the environment #
#######################
if (!$ENV{'MP_SET_NUMTHREADS'} ) {$ENV{'MP_SET_NUMTHREADS'}  = 'all';}
if (!$ENV{'MP_SLAVE_STACKSIZE'}) {$ENV{'MP_SLAVE_STACKSIZE'} = '134217728';}
if (!$ENV{'MPC_GANG'}          ) {$ENV{'MPC_GANG'}           = 'off';}
if (!$ENV{'OMP_NUM_THREADS'}   ) {$ENV{'OMP_NUM_THREADS'}    = 'all';}
if (!$ENV{'OMP_DYNAMIC'}       ) {$ENV{'OMP_DYNAMIC'}        = 'FALSE';}
#  if (!$ENV{'DATAPATH'}          ) {$ENV{'DATAPATH'}           = '/usr/projects/data/nuclear/mc/type1';}

$RR_EXECUTABLE = $MCNP;
if ($MPI eq 'yes' ) 
{
    $MCNP = "$PRUN $MCNP";
}

if ( $DEBUG ) 
{
    print " \n";
    print " Using module init file: $MODULESHOME/init/perl\n";
    print " Loading modules :: load modules\n";
    print " Loading modules :: load $MODULES\n";
    print " Execution statement: $MCNP @USR_ARGS $EOL\n";
    print " \n";
    print " *********************************************************\n";
    print " *********************************************************\n";
    print " \n";
}

################################
# Load the appropriate modules #
################################
#  &module("load friendly-testing");
&module("load $MODULES");
&module("list");

###################
# Execute the job #
###################
my $execution_line = "$MCNP @USR_ARGS $EOL";

$cmdstrg = "$shell -c $UNLIMIT; $execution_line;";
print "executing: $cmdstrg\n";
$start = Time::HiRes::gettimeofday();
# Use system call instead of exec, since there is no return from exec and
# we need to come back to compute the elapsed time and print the run info
my $run_result = system( $cmdstrg);
$end = Time::HiRes::gettimeofday();

$elapsed = $end - $start;
$elapsed = sprintf("%.2f", $elapsed);
print "\nElapsed time: $elapsed seconds\n";

##################
# print_run_info #
##################
if ($PRINTRUNINFO) {
    # get just the executable file name off of the end
    my @parts = split( "/", $RR_EXECUTABLE );
    my $executable = $parts[-1];
    PRINT_run_info::PRINT_all_run_info("mcnp", $executable, $MCNPVERSION, 
				       $reqNP, $reqTASKS, $NP,
				       $TASKS, $elapsed, $run_result);
}
exit;

#############################################################################

# need this to get actual executable names for bleeding edge
# since they are links to the most recent versions.
sub get_exec_name {
    my $dir = shift;
    my $exec = shift;

    my $fullname = $dir . "/" . $exec;
    my $actualname = `ls -l $fullname`; # get what link is pointing to
    my @parts = split("/", $actualname);

    my $justexec = $parts[-1]; # get just the executable name
    $justexec =~ s/\r|\n//g; # get rid of carriage returns
    return $justexec;
}

sub validate_user {
    my $grp_chk = shift;

    my $groups = `groups`;
    my $i = index($groups, $grp_chk);
    if ($i < 0) 
    {
	print <<"end_of_sorry";
      ************************************************************************
      
      You are not a member of the mcnp unix group and need to be properly
      vetted in order to use MCNP on this system.
      
      Please contact an MCNP group administrator:
                                             Chris Werner   - cwerner\@lanl.gov
                                             Jeff Bull      - jsbull\@lanl.gov
                                             Laura Casswell - casswell\@lanl.gov
      
      ************************************************************************

end_of_sorry

         exit;
    }
    return;
}

sub man {

print <<MAN;
NAME
       mcnp5/mcnp6/mcnpexe - mcnp perl wrapper, sets up the environment and
                             runs the correct version of MCNP5/6, including
                             the bleeding edge version of MCNP6.

SYNOPSIS
       mcnp5/mcnp6/mcnpexe [SCRIPT OPTIONS]... [MCNP FILES]... [MCNP STANDARD OPTIONS]... 

EXAMPLE
       mcnp5 inp=inp01

         This will execute a single (non-MPI, non-OpenMP) MCNP process.

       mcnp5 -np 25 inp=inp01 out=out01 run=run01 tasks 4

         This will execute MCNP with 1 master MPI process and 24 slave MPI 
         processes and 4 threads for each slave MPI process for a total of
         96 slave processes transporting particles.
      
       mcnp5.mpi inp=inp01      (or)
       mcnp5 -np all inp=inp01

         These commands will execute MCNP via MPI using all job queue resources 
         to which the user is subscribed.

DESCRIPTION
       Runs the latest version of MCNP5/MCNP6. This script sets up the users 
       environment correctly on the LANL production machines: moonlight and
       mapache. This script ensures that the user has allocated resources,
       correctly sets up the user enviroment by loading the same modules with
       which MCNP was built, and launchs the correct version of MCNP.

       This script will also launch either mpirun for the user if the user
       uses the -np option or uses the mcnp5.mpi or mcnp6.mpi link to the
       script.

SCRIPT OPTIONS

       -5
              last stable version of mcnp5

       -6
              last stable version of mcnp6

       -be
              the latest bleeding edge version of mcnp6
              (i.e., from the CVS repository at the preceeding day\'s COB)
              Overrides options -5, -6, -exec, -mcnp, -mcnp5, -mcnp6.

       -debug, -verbose, -v
              print debugging information

       -exec, -mcnp, -mcnp5, -mcnp6  /path_to/mcnp
              Used to override the default mcnp executable (Options -5 and -6).  
              The argument that follows is the mcnp executable (including full path) 
              to be used.

       -execlist
              List the executables that will be used for: mcnp5, mcnp6, and the
              bleeding edge, as well as the directories they reside in.

       -help, --help, -man
              Prints this help message.

       -np [m]
              Uses MPI where [m] is the total number of MPI processes, including
              the master, and [m]-1 slave processes will track the particles. 
              Note that the minimum number of slaves accepted by MCNP is two, so
              at least three MPI processes must be initiated. That is, <m> can 
              equal 1 or be greater than or equal to 3. 

       -np all
             Uses all LSF resources to which the user is subscribed.

MCNP FILES

       MCNP uses several files for input and output.  The files pertinent to 
       the sample problem are shown in the table below.  File INP must be 
       present as a local file.  MCNP will create OUTP and RUNTPE.

       DEFAULT FILE NAME   DESCRIPTION
       -----------------   -----------
       INP                 Problem input specification
       OUTP                BCD output for printing
       RUNTPE              Binary start-restart data
       XSDIR               Cross-section directory

       The default name of any of the files in Table 1.2 can be changed on the 
       MCNP execution line by entering

          default_file_name=newname

       For example, if you have an input file called "mcin" and want the output 
       file to be "mcout" and the runtpe to be "mcruntpe", the execution line is

          mcnp5 inp=mcin outp=mcout runtpe=mcruntpe
 
       Only enough letters of the default name are required to uniquely identify
       it. For example,

          mcnp5 i=mcin o=mcout ru=mcrntpe

       also works. If a file in your local file space has the same name as a 
       file MCNP needs to create, the file is created with a different unique
       name by changing the last letter of the name of the new file to the next
       letter in the alphabet. For example, if you already have an "outp", MCNP 
       will create "outq".

      Sometimes it is useful for all files from one run to have similar names. 
      If your input file is called JOB1, the following line

          mcnp5 name=job1

      will create an OUTP file called JOB1O and a RUNTPE file called JOB1R. If
      these files already exist, MCNP will NOT overwrite them or modify the last
      letter, but will issue a message that JOB1O already exists and then will 
      terminate.

MCNP OPTIONS

   Module Execution Mnemonics - See manual Vol II p.1-13
 
       Mnemonic    Module   Operation
       --------    ------   ---------
          i     -  IMCN     Process problem input file 
          p     -  PLOT     Plot geometry
          x     -  XACT     Process cross sections
          r     -  MCRUN    Particle transport
          z     -  MCPLOT   Plot tally results or cross section data

       Default mnemonic is ixr.
       Use i to look for input errors.
       Use ip to debug geometry by plotting
       Use ixz to plot cross-section data
       Use z to plot tally results from the RUNTPE or MCTAL files.
        
   Other Options Mnemonics

       Mnemonic   Operation
       --------   ---------
       C m        Continues a run starting with mth dump. If m is omittd, the
                  last dump is used. See Vol. II p. 3-2.
       CN         Like C, but dumps are written immediately after the fixed part
                  of the RUNTPE, rather than at the end. See page 3-2.
       DBUG n     Writes debug information every n particles. See DBCN card, 
                  page 3-138.
       NOTEK      Indicates that your terminal has no graphics capability. PLOT
                  output is in PLOTM.PS. Equivalent to TERM=0. See Appendix B 
                  for details.
       FATAL      Transports particles and calculates volumes even if fatal 
                  errors are found.
       PRINT      Creates the full output file; equivalent to PRINT card. See 
                  page 3-142.
       TASKS n    Invokes OpenMP threading on shared memory systems.  
                  n=number of threads to be used.
       BALANCE    Provides load balancing when used with MPI.
MAN
1;
}
