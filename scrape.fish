#!/usr/local/bin/fish
set startIdx 593
for i in (seq 10)
    set pageNumber (math $startIdx+$i)
    curl https://na.op.gg/ranking/ladder/page=$pageNumber > temp.html
    cat temp.html | grep -o 'userName=.*' | cut -f 2 -d = | cut -f 1 -d '"' >> names.txt
end
