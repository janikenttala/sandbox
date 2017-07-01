#!/bin/sh

myerr() {
    echo $* 1>&2
    exit 1
}

[[ $# -eq 2 ]] || myerr "$0: <user> <key>"
user=$1
key=$2

i=1; curl -u "${user}:${key}" "https://api.github.com/users/${user}/events?page=${i}&per_page=100"  >app/data/${i}.json
sh timeline.sh app/data/1.json| sort -rn | python joiner.py > app/data/timeline.json

cd app
python3 -m http.server --bind 127.0.0.1