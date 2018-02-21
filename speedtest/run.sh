while true
do
    speedtest-cli --json |python speed2cloud4rpi.py
    sleep 300
done

#cat example.json |python speed2cloud4rpi.py