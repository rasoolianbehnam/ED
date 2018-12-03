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
    javac *.java && java $filename "curl 'https://cdn.mcloud.to/stream/sf:i0:q2:h0:p26:l1/ZYBdXIqy_Q8g_w3axi1wXg/1543899600/g/0/5/3rz948/hls/480/480-(0561).ts' -H 'origin: https://mcloud.to' -H 'accept-language: en-US,en;q=0.9' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.116' -H 'accept: */*' -H 'referer: https://mcloud.to/embed/@9@P894495M0EP35?sub.file=https%253A%252F%252Fwww6.putlockertv.to%252Fsubtitle%252F29804.vtt&ui=pQh9%406j17vsGg4%40YeqMZsJgrq%2FSdUPy9xT7fNq%403%40A%3D%3D&autostart=true' -H 'authority: cdn.mcloud.to' -H 'cookie: __cfduid=d24e48d19464c5d3edb3f66e99765cf9c1543786159; _ga=GA1.2.1075411393.1543786162; _gid=GA1.2.1709130335.1543786162; _gat=1' --compressed" 2 4
    ;;
*)
    echo "Extension not supported..."
    ;;

esac
