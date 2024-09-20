#!/bin/bash


FAST_API_HOST="127.0.0.1" #-h
FAST_API_PORT="9128" #-p
DB_HOST="mm_db_tb_cont" #-H
DB_PORT="5432" #-P
DB_PASS="pass" #-s
DB_DB="postgres" #-d
DB_USER="postgres" #-u


while getopts 'h:H:p:P:s:d:u:' opt; do
    case "$opt" in
        h)
            FAST_API_HOST="$OPTARG";;
        H)
            DB_HOST="$OPTARG";;
        p)
            FAST_API_PORT="$OPTARG";;
        P)
            DB_PORT="$OPTARG";;
        s)
            DB_PASS="$OPTARG";;
        d)
            DB_DB="$OPTARG";;
        u)
            DB_USER="$OPTARG";;
    esac
done


echo "FAST_API_HOST -> ${FAST_API_HOST}"
echo "FAST_API_PORT -> ${FAST_API_PORT}"
echo "DB_HOST -> ${DB_HOST}"
echo "DB_PORT -> ${DB_PORT}"
echo "DB_PASS -> ${DB_PASS}"
echo "DB_DB -> ${DB_DB}"
echo "DB_USER -> ${DB_USER}"

export FAST_API_HOST=${FAST_API_HOST}
export FAST_API_PORT=${FAST_API_PORT}
export DB_HOST=${DB_HOST}
export DB_PORT=${DB_PORT}
export DB_DB=${DB_DB}
export DB_USER=${DB_USER}
export DB_PASS=${DB_PASS}


docker container rm -f mm_tb_db_cont
python3 app.py &
docker run --name mm_tb_db_cont --rm -p ${DB_PORT}:${DB_PORT} -e POSTGRES_PASSWORD=${DB_PASS} timescale/timescaledb-ha:pg16   
