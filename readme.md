Program Function: (connect host machine to docker container)
    1. run a fast api default at localhost:9128
    2. stores data in timescaledb 
    3. there is only one docker image timescaledb 

How to run: 
    1. ./run.sh 
    2. arguments you can pass are 
    3. -h -> host for fast api 
    4. -H -> host for db 
    5. ./run.sh -h 127.0.0.1 -H mm_db_tb_cont 
    6. other args can be found in the run.sh file 
    7. open 127.0.0.1:9128 in chrome to enter data 
    8. open 127.0.0.1:9128/view to get all the data 
    
