ssh root@vpn "cd maid-bot && docker compose stop && git pull"
cat tokens.env | ssh root@vpn "cat > maid-bot/tokens.env && cd maid-bot && docker compose up --build"