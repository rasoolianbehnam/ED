clear&&clear
fileName=$(echo $i | cut -d'.' -f1)
if [[ $1 = *.cu ]]; 
then 
    nvcc $1 -o ${fileName}_cu && ./${fileName}_cu;
elif [[ $1 = *.py ]]; 
then
    python $1;
elif [[ $1 = *.c* ]]; 
then
    #echo clang++ $1 -o ${fileName}_cpp | bash -x && echo ./${fileName}_cpp | bash -x
    echo gcc -c $1 -o tmp.o | bash -x && echo gcc -static tmp.o -lm -o ${fileName}.out | bash -x && echo ./${fileName}.out | bash -x

fi
