#!/bin/bash
# vars needed:  infile  count   pname   dith    pause           -f  -c  -n  -d  -p

function get_infile {
    INFILE=$(whiptail --inputbox "What is the name of the input file?" 8 78 --title "APT XML" 3>&1 1>&2 2>&3)
}

function get_count {
    COUNT=$(whiptail --inputbox "How many exposures would you like to take?" 8 78 10 --title "APT XML" 3>&1 1>&2 2>&3)
}

function get_pname {
    PNAME=$(whiptail --inputbox "What would you like the program name to be?" 8 78 "ASI_294MC_Pro_Cool_"  --title "APT XML" 3>&1 1>&2 2>&3)
}

function get_dith {
    if (whiptail --title "APT XML" --yesno "Would you like to use dithering?" 8 78); then
        DITH="y"
    else
        DITH="n"
    fi
}

function get_pause {
    PAUSE=$(whiptail --inputbox "How long would you like to wait between exposures?" 8 78 5 --title "APT XML" 3>&1 1>&2 2>&3)
}

function generating_file {
    {
    for ((i = 0 ; i <= 100 ; i+=5)); do
        sleep 0.1
        echo $i
    done
    } | whiptail --gauge "Please wait while file is generated..." 6 50 0
}

function file_generated {
    whiptail --title "APT XML" --msgbox "File $PNAME has been generated." 8 78
}

#Initial welcome screen
whiptail --title "APT XML" --msgbox "Welcome to APT XML Plan Generator. You must hit OK to continue." 8 78


if (whiptail --title "APT XML" --yesno "Would you like to use the default settings?" 8 78); then
    #Default settings
    get_infile
    command python3 continue_imaging.py -f $INFILE
    generating_file
    file_generated
else
    #Custom settings, will add a checklist style selection to define which settings to mod from default.
    get_infile
    get_count
    get_pname
    get_dith
    get_pause
    command python3 continue_imaging.py -f $INFILE -c $COUNT -n $PNAME -d $DITH -p $PAUSE
    generating_file
    file_generated
fi


