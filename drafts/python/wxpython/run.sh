clear && clear
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    python $@
elif [[ "$OSTYPE" == "darwin"* ]]; then
    pythonw $@
fi
