python3 -u -m agents.oracle "$1" "$2" "$3" 2>&1 | tee ./logs/oracle.txt &
python3 -u -m participants.p1 "$1" "$2" "$3" 2>&1 | tee ./logs/p1.txt &
python3 -u -m participants.p2 "$1" "$2" "$3" 2>&1 | tee ./logs/p2.txt &
python3 -u -m participants.p3 "$1" "$2" "$3" 2>&1 | tee ./logs/p3.txt &
python3 -u -m participants.p4 "$1" "$2" "$3" 2>&1 | tee ./logs/p4.txt &
python3 -u -m participants.p5 "$1" "$2" "$3" 2>&1 | tee ./logs/p5.txt &
python3 -u -m participants.p6 "$1" "$2" "$3" 2>&1 | tee ./logs/p6.txt &
echo "started oracle and 7 participants"
