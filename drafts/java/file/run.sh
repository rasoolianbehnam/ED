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
    javac *.java && java $filename "curl 'https://zeus.streamvid.co/tsfiles/IEADDEBI/1080K/2018/EGFIAAHB/01/CEDHDGIE/07/EFFBGACB/01911-(001).ts' -H 'origin: https://streamvid.co' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.104' -H 'accept: */*' -H 'referer: https://streamvid.co/player/HLRvDF4a4OEpmkT/' -H 'authority: zeus.streamvid.co' --compressed" 658 5
    ;;
*)
    echo "Extension not supported..."
    ;;

esac
