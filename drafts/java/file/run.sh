clear && clear
echo 'Running global run.sh'
DIR=$(dirname "$1")
filename=$(basename -- "$1")
extension="${filename##*.}"
filename="${filename%.*}"

#if [ $extension = 'py' ]; then
#    python $1
#elif [ $extension = 'c' ]; then
#    gcc -o $DIR/$filename.out $1 && $DIR/$filename.out
#fi

case $extension in
"py")
    python $1
    ;;
"c")
    gcc -o $DIR/$filename.out $1 && $DIR/$filename.out
    ;;
"tex")
    pdflatex $1 && bibtex $filename.aux
    ;;
"java")
    javac *.java && java $filename "curl 'https://hawk.streamvid.co/tsfiles/CAIIHFHA/1080K/2018/IHFCHCCC/10/FBDFDFAB/30/DABECFEE/83999-(006).ts' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://streamvid.co/player/temXADwgQAf0NrX/' -H 'Origin: https://streamvid.co' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'TE: Trailers'" 10 4
    ;;
*)
    echo "Extension not supported..."
    ;;

esac
