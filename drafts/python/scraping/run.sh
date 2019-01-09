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
    python $1 "curl 'https://stream-2-1.loadshare.org/stream/VideoID-paUdS4HH/tB-VvD_N4r8SqzCvaHLkHZo8yFG5ozkVhABiEzjOEFsdImHUiO69O5FNd907lQ75muVCsGNMLndbpFnA4KJZ1-qNO7oU8DtbOaewDfi_a4AYiS_UatMw6UQva_8w5WTinD1ltER7_S3oon6rY8sQOQ/seg-(1593)-f2-v1-a1.ts?token=ip=97.80.234.110~st=1546656494~exp=1546670894~acl=/*~hmac=ea3c46c42b007a01f714d2539f0739f42ffbdb7adabc45355a115fb815eb5609' -H 'origin: https://putlocker.digital' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.106' -H 'accept: */*' -H 'referer: https://putlocker.digital/movie/everybody-knows-todos-lo-saben/DeGXXMD7/bGojtTlZ-watch-online-free.html' -H 'authority: stream-2-1.loadshare.org' --compressed" %d 524 8

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
