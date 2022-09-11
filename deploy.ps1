ssh root@vpn "cd maid-bot && docker compose stop && git pull"
ssh root@vpn "cd maid-bot && docker compose up --build"
cat .env | ssh root@vpn "cat >> maid-bot/.env  && cd maid-bot && docker compose up --build"