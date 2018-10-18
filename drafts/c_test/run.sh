#clear && clear
#make clean
#fileName=$(echo $1 | cut -d'.' -f1)
#echo $fileName
##make
#echo gcc -g -o ${fileName}.out $1 | bash -x
#echo ./${fileName}.out | bash -x

file_name=$(basename $1)
base=${file_name%.*}
extension=${file_name##*.}

gcc -g -o $base $1 && ./$base
