#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)
#echo "this is ${bold}bold${normal} but this isn't"

mj_act () {
echo Activating...
source activate
}


#c.InteractiveShellApp.exec_files = [
#    'test.py'
#]


printf "\n"
echo "MJ launcher"
echo "Note: PYTHONPATH is currently set to:"


MANPATH=$PATH

# Replace colons with spaces to create list.
for thispath in ${MANPATH//:/ }; do
    echo "$thispath"
done


#echo $PATH
#printf "\nChoose an envi"

printf "\n"


conda env list


printf "\nChoose environment by letter:\n"
#printf "${bold}b${normal}ase, ${bold}a${normal}tom, ${bold}s${normal}spark, s${bold}c${normal}rape, ${bold}n${normal}o change\n"
printf "${bold}b${normal}ase, ${bold}s${normal}park, ${bold}d${normal}eep, ${bold}n${normal}o change\n"
read -n1 -p "Choose env:" doit 
case $doit in
    B|b) printf "\nActivating base environment \n"  
        mj_act base
        ;;      
    S|s) printf "\nActivating spark environment \n"  
        mj_act spark
        ;;
    D|d) printf "\nActivating deep environment \n"  
        mj_act deep
        ;;      
  *) printf "\nEnvironment unchanged \n"  ;; 
esac


conda env list

#printf "${bold}a${normal}tom, ${bold}j${normal}upyter, j-${bold}L${normal}ab, ${bold}c${normal}onsole \n"
printf "j-${bold}L${normal}ab \n"

read -n1 -p "Choose program to start:" doit 
case $doit in  
    #A|a) printf "\n Starting atom \n"
#       atom
#       ;; 
    #J|j) printf "\n Starting jupyter notebook\n"  
    #   jupyter notebook --notebook-dir="/home/batman/git/ref_DataScienceRetreat/DSR Lecture notebooks"
   #    ;; 
    L|l) printf "\n Starting Jupyter Lab \n"  
            jupyter-lab --notebook-dir="/home/batman/git/ref_DataScienceRetreat/DSR Lecture notebooks"
        ;;  
    #C|c) printf "\n Returning back to console \n"  
   #    ;;
#   
  *) printf "No program selected, returning back to console \n" ;; 


esac






