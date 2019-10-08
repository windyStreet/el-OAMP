#!/bin/bash

rm -rf /usr/longrise/LEAP/*
mkdir -p /usr/longrise/LEAP/YXYBB/WEB-INF
mkdir -p /usr/longrise/LEAP/LSIP/WEB-INF
mkdir -p /usr/longrise/LEAP/INSY125/WEB-INF

\cp /data/smbshare/【运维相关】/pressureTest/YXYBB/* /usr/longrise/LEAP/YXYBB/WEB-INF -r
\cp /data/smbshare/【运维相关】/pressureTest/LSIP/* /usr/longrise/LEAP/LSIP/WEB-INF -r
\cp /data/smbshare/【运维相关】/pressureTest/INSY125/* /usr/longrise/LEAP/INSY125/WEB-INF -r

chown -R tomcat:tomcat /usr/longrise/LEAP/YXYBB/WEB-INF
chown -R tomcat:tomcat /usr/longrise/LEAP/LSIP/WEB-INF
chown -R tomcat:tomcat /usr/longrise/LEAP/INSY125/WEB-INF

dbback_path=/data/smbshare/project_DB/192.168.7.212/2018-01-08
array=( lupdpstudyex LUPDP_VIP LSIPTEST_fee LSIPTEST_train LSIPTEST_services LUPDP_VIP_SCORE LSIPTEST_basedataex0526 LSIPTEST_person LSIPTEST_cert LSIPTEST_credit ACC_DEV LSIPTEST_exam LSIPTEST_trainrecord LSIPTEST_trainresource_2 lupdponlinetest0721 LSIPTEST_dev LSIPTEST_credit0318 LSIPTEST_fee_20170210 LSIPTEST_trainresource_1 insy_test_170321 LSIPTEST_basedataex0526 hnis_0620 )
for var in ${array[@]};
do
    echo ${var}
    cd /data/smbshare/project_DB/192.168.7.212/2018-01-08
    tar -zxvf ${var}*.tar.gz
    ll /data/smbshare/project_DB/192.168.7.212/2018-01-08/${var}*.tar.gz

    psql -h localhost -p 54320 -U postgres -d postgres -c 'create database '${var}
    echo '创建'${var}'数据库成功'
    pg_restore -h localhost -p 54320 -U postgres -d "$var"  < ${dbback_path}/${var}*.backup
    echo '恢复'${var}'数据库成功'
done
var1='insy125_test170104'
cd /data/smbshare/project_DB/192.168.7.212/2018-01-08
tar -zxvf ${var2}*.tar.gz
pg_restore -h localhost -p 54320 -U postgres -d "INSYI125_LEAP_20180108"  < ${dbback_path}/${var}*.backup
echo '恢复'${var1}'数据库成功'
var2='LSIPTEST-LEAP-20161117'
cd /data/smbshare/project_DB/192.168.7.212/2018-01-08
tar -zxvf ${var2}*.tar.gz
pg_restore -h localhost -p 54320 -U postgres -d "LSIP_LEAP_20180108"  < ${dbback_path}/${var2}*.backup
echo '恢复'${var2}'数据库成功'
var3='LUPDP_TEST'
cd /data/smbshare/project_DB/192.168.7.212/2018-01-08
tar -zxvf ${var3}*.tar.gz
pg_restore -h localhost -p 54320 -U postgres -d "YXYBB_LEAP_20180108"  < ${dbback_path}/${var3}*.backup
echo '恢复'${var3}'数据库成功'

