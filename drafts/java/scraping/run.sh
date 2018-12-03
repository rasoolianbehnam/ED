clear && clear
rm *.ts
#rm *.jpg
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
    python $1 "curl 'https://s10.7btj.xyz/hls/qvsbeqpfn3blgwsztrjka6g6lwtozuzrir4ygxmd24nigtzc5p3uxbwfi4sq/seg-(371)-v1-a1.jpg' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://putlocker9.nl/film/harry-potter-and-the-sorcerer-s-stone-2001-1080p.93432/watching.html' -H 'Origin: https://putlocker9.nl' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'TE: Trailers'" %d 5000 8

    ;;
"c")
    gcc -o $DIR/$filename.out $1 && $DIR/$filename.out
    ;;
"tex")
    pdflatex $1 && bibtex $filename.aux
    ;;
"java")
    javac *.java && java $filename "curl 'https://s10.7btj.xyz/hls/qvsbeqpfn3blgwsztrjka6g6lwtozuzrir4ygxmd24nigtzc5p3uxbwfi4sq/seg-(1)-v1-a1.jpg' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://putlocker9.nl/film/harry-potter-and-the-sorcerer-s-stone-2001-1080p.93432/watching.html' -H 'Origin: https://putlocker9.nl' -H 'Connection: keep-alive' -H 'DNT: 1'" 2 4
    ;;
*)
    echo "Extension not supported..."
    ;;

esac
