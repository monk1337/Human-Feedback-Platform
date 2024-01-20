#!/bin/bash

docker compose exec mongo1 mongosh --port 27021 --quiet --eval "rs.initiate({_id:'rs_insightflow',members:[{_id:0,host:'vc-mongo1:27021',priority:1},{_id:1,host:'vc-mongo2:27022',priority:0.5},{_id:2,host:'vc-mongo3:27023',priority:0.5}]})" --json relaxed
