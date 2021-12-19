#!/bin/bash

deploy_path='/home/pi/deploy'
project_name='didier-python'
home_path='home:/home/david/Nextcloud/rosita/python/'$project_name

rm -rf $deploy_path/$project_name
rsync -rtvu --delete $home_path $deploy_path
cd $deploy_path
echo "exec : "$deloy_path/$project_name/$1
python3 $deploy_path/$project_name/$1