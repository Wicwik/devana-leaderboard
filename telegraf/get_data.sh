#!/bin/bash
# put this file in the home directory of data fetcher user

# projects to check
projects=(p904-24-3)

get_kinit_usage_raw() {
    scontrol -o show assoc_mgr | grep "Account=$1 UserName= Partition=" | awk '{print $8}' | awk -F/ '{print $3}' | sed -e 's/Efctv=//g'
}

get_users() {
    sacctmgr -np show association where account=$1 | cut -f3 -d\| | awk NF
}

get_gpu_usage_raw() {
    scontrol -o show assoc_mgr | grep "Account=$1 UserName=$2" | awk '{print $8}' | awk -F/ '{print $3}' | sed -e 's/Efctv=//g'
}

used_raw_sum=0
used_hour_sum=0

for project in ${projects[@]};
do
    kinit_usage_raw=`get_kinit_usage_raw $project`;
    kinit_usage_hour=`echo $kinit_usage_raw/57600 | bc`;
    used_raw_sum=`echo $used_raw_sum + $kinit_usage_raw | bc`
    used_hour_sum=`echo $used_hour_sum + $kinit_usage_hour | bc`

    echo "gpu,project=$project,user=kinit used_raw=$kinit_usage_raw,used_hour=$kinit_usage_hour `date +%s%N`";
    for user in `get_users $project`;
    do
        gpu_usage_raw=`get_gpu_usage_raw $project $user`;
        gpu_usage_hour=`echo $gpu_usage_raw/57600 | bc`;

        echo "gpu,project=$project,user=$user used_raw=$gpu_usage_raw,used_hour=$gpu_usage_hour `date +%s%N`"
        used_raw_sum=`echo $used_raw_sum + $gpu_usage_raw | bc`
        used_hour_sum=`echo $used_hour_sum + $gpu_usage_hour | bc`
    done
done

echo "gpu,project=$project used_raw_total=$used_raw_total,used_hour_total=$used_hour_sum `date +%s%N`"