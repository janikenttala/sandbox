# Running

```shell
user=<your github user>
key=<your github app key>
i=1; curl -u "${user}:${key}" "https://api.github.com/users/${user}/events?page=$i&per_page=100"  >app/data/$i.json
sh timeline.sh app/data/1.json| sort -rn | python joiner.py > app/data/timeline.json
```
