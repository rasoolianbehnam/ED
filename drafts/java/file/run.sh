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
    javac *.java && java $filename "curl 'https://cnnios-f.akamaihd.net/i/cnn/big/world/2016/08/19/mexico-search-for-el-chapo-son-romo-pkg.cnn_718241_ios_,440,650,840,1240,3000,5500,.mp4.csmil/segment(006)_4_av.ts?null=0' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Origin: https://www.cnn.com' -H 'Connection: keep-alive' -H 'DNT: 1'"
    ;;
*)
    echo "Extension not supported..."
    ;;

esac
