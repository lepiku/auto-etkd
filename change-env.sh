#! /bin/bash

# added by Anaconda3 5.3.0 installer, taken from .bashrc
# >>> conda init >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$(CONDA_REPORT_ERRORS=false '/home/dimas/Programs/anaconda3/bin/conda' shell.bash hook 2> /dev/null)"
if [ $? -eq 0 ]; then
    \eval "$__conda_setup"
else
    if [ -f "/home/dimas/Programs/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/dimas/Programs/anaconda3/etc/profile.d/conda.sh"
##        CONDA_CHANGEPS1=false
        conda activate std
    else
        \export PATH="/home/dimas/Programs/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda init <<<

python3 ~/Dropbox/Python/auto-etkd/etkdbkd.py

echo "[END OF PROGRAM]"
#read
