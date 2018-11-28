dirname=$(dirname -- "$1")
filename=$(basename -- "$1")
extension="${filename##*.}"
filename="${filename%.*}"
echo $dirname
clear && javac $1 && java $filename
