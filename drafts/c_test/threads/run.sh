#clang++ test.cpp -o test && ./test
#clang++ potential.cpp -o potential && ./potential
#nvcc add2.cu -o add2_cu && ./add2_cu
#nvcc add3.cu -o add3_cu && ./add3_cu
#nvprof python $1
clear&&clear
echo "using global file"
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
    echo gcc -o ${fileName}.out $1 | bash -x && echo ./${fileName}.out | bash -x

fi
