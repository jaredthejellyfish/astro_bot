# -----------------------------------------------------------
# Generates a continuation to prior APT plan from FIT file Whiptail GUI
#
# (C) 2020 Gerard Almenara, Barcelona, Spain
# Released under GNU Public License (GPL)
# Email: jarredthejellyfish@gmail.com
#
# Whiptail wiki: https://en.wikibooks.org/wiki/Bash_Shell_Scripting/Whiptail#Password_box
# -----------------------------------------------------------

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

function error_message {
    whiptail --title "APT XML" --msgbox "Damn, there was an error generating your file. Hit OK to exit the program and relaunch it to try again." 8 78
}

rm -rf *.xml

#Initial welcome screen
whiptail --title "APT XML" --msgbox "Welcome to APT XML Plan Generator. You must hit OK to continue." 8 78

if (whiptail --title "APT XML" --yesno "Would you like to use the default settings?" 8 78); then
    #Default settings
    get_infile
    if ! command python3 continue_imaging.py -f $INFILE;then
        error_message
    else
        generating_file
        echo -e "\033[0;33mScript executed successfully. Clear skies!\0033[0m"
        file_generated
    fi 2>/dev/null
    
else
    #Custom settings, will add a checklist style selection to define which settings to mod from default.
    get_infile
    get_count
    get_pname
    get_dith
    get_pause
    if ! command python3 continue_imaging.py -f $INFILE -c $COUNT -n $PNAME -d $DITH -p $PAUSE;then
        error_message
    else
        generating_file
        echo -e "\033[0;33mScript executed successfully. Clear skies!\0033[0m"
        file_generated
    fi 2>/dev/null
fi




