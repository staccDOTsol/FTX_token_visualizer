header="../header.txt"
for file in ./*.csv
do
    cat "$header" "$file" > /tmp/xx.$$
    mv /tmp/xx.$$ "$file"
done


