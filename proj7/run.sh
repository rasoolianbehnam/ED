fileName=$(echo $1 | cut -d'.' -f1)
extension=$(echo $1 | cut -d'.' -f2)
echo file name: $fileName
echo extension: $extension
if [ $extension = 'py' ]; then
    echo python $1 | bash -x;
elif [ $extension = 'c' ]; then
    echo gcc -g -static -m32 -z execstack -no-pie -fno-stack-protector -o $fileName.out $1 | bash -x
    #echo gcc -g -m32 -z execstack -no-pie -fno-stack-protector -o $fileName.out $1 | bash -x
    echo ./${fileName.out} | bash -x
fi
