clear && clear
#make clean
#fileName=$(echo $1 | cut -d'.' -f1)
#echo $fileName
##make
#echo gcc -g -o ${fileName}.out $1 | bash -x
#echo ./${fileName}.out | bash -x
array=( $@ )
len=${#array[@]}
args=${array[@]:1:$len}
echo $args

file_name=$(basename $1)
base=${file_name%.*}
extension=${file_name##*.}

<<<<<<< HEAD
gcc -g -o ${base}.out $1 && ./${base}.out
=======
#echo "gcc -g -m32 -o $base.out $1 && ./$base.out $args" | bash -x
gcc -g -m32 -o $base.out $1 && ./$base.out $args
>>>>>>> f445fef6e1a71af8de36721870ce4248794ed481
