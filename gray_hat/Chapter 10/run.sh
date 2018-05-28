fileName=$(echo $1 | cut -d'.' -f1)
extension=$(echo $1 | cut -d'.' -f2)
echo file name: $fileName
echo extension: $extension
if [ $extension = 'py' ]; then
    echo python $1 | bash -x;
elif [ $extension = 'c' ]; then
    echo gcc -o $fileName.out $1 | bash -x;
fi
