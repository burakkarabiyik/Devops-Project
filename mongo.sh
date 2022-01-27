#!/bin/bash
mongobaglanti="mongosh  --host 127.0.0.1 --authenticationDatabase 'admin' --username 'root' --password 'password' --eval 'quit()'"
while :
do
variable=$(${mongobaglanti})
var=$(echo $variable | grep -c "Using")
if [ "$var" -gt "0" ];
then
    /bin/mongosh  127.0.0.1 --authenticationDatabase 'admin' --username 'root' --password 'password' <<EOF
        
        aa={_id:'mydb-replica-set',members:[{_id:0,host:'mydb-0:27017',priority:2},{_id:1,host:'mydb-1:27017',priority:1},{_id:2,host:'mydb-2:27017',priority:1}]}
        rs.initiate(aa,{force: true})
        rs.reconfig(aa, { force: true })
        
        quit()
        
EOF
break
else
    echo "baglantı yok"
fi
done