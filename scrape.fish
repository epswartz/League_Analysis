#!/usr/local/bin/fish

# Scrapes the leaderboard of op.gg for usernames.
set startIdx 594 # As of 11/5/2019, the first page of all P1
set skipFactor 10 # Reads from every skipFactorth page - we can spread out the reads so we don't have a continuous zone of the ladder
for i in (seq 10)
    set idx (math "$skipFactor * $i")
    set pageNumber (math $startIdx+$idx)
    curl https://na.op.gg/ranking/ladder/page=$pageNumber > temp.html
    cat temp.html | grep -o 'userName=.*' | cut -f 2 -d = | cut -f 1 -d '"' >> names.txt
    rm temp.html
end
