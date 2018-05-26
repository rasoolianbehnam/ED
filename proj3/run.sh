fileName=$(echo $1 | cut -d'.' -f 1)
gcc -g -static -m32 -z execstack -no-pie -fno-stack-protector -o $fileName.out $1
