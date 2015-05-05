#!/bin/bash

TIME=$(date +%Y-%m-%d_%H:%M:%S)
DATE=$(date +%Y-%m-%d)
path='/home/mgmt/update_52_iplay_data'

if [ -d "$path/$DATE" ];
then
rm -rf  $path/$DATE
fi
if [ -d "$path/$DATE.tar.gz" ];
then
rm -rf  $path/$DATE.tar.gz
fi

echo $TIME',Bash shell: start dump data from 178'

if [ ! -d "$path/$DATE" ];
then
mkdir -p $path/$DATE
fi
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_category_game_order_adjust > $path/$DATE/iplay_category_game_order_adjust_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_category_to_game_result > $path/$DATE/iplay_category_to_game_result_$DATE.sql
#mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_config > $path/$DATE/iplay_config_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_game_category_info > $path/$DATE/iplay_game_category_info_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_game_label_to_pkg_result > $path/$DATE/iplay_game_label_to_pkg_result_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_hot_search_words > $path/$DATE/iplay_hot_search_words_$DATE.sql
#mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_id_url_pkg > $path/$DATE/iplay_id_url_pkg_$DATE.sql
#mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_id_url_pkg_newgen > $path/$DATE/iplay_id_url_pkg_newgen_$DATE.sql
#mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_products > $path/$DATE/iplay_products_$DATE.sql
#mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_products_privilege_imei > $path/$DATE/iplay_products_privilege_imei_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_recomend_banner_info > $path/$DATE/iplay_recomend_banner_info_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_recomend_game > $path/$DATE/iplay_recomend_game_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_resource_match_result > $path/$DATE/iplay_resource_match_result_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_topic_game > $path/$DATE/iplay_topic_game_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_topic_info > $path/$DATE/iplay_topic_info_$DATE.sql
#mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_upload_game > $path/$DATE/iplay_upload_game_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum pre_iplay_game_resource_info > $path/$DATE/pre_iplay_game_resource_info_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum pre_iplay_game_resource_author > $path/$DATE/pre_iplay_game_resource_author_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum pre_iplay_game_resource_match_condition > $path/$DATE/pre_iplay_game_resource_match_condition_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_billboard_info > $path/$DATE/iplay_billboard_info_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_game_forecast_info > $path/$DATE/iplay_game_forecast_info_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_forecast_to_label_result > $path/$DATE/iplay_forecast_to_label_result_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_game_developer > $path/$DATE/iplay_game_developer_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_category_info > $path/$DATE/iplay_category_info_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_game_compatibility_model > $path/$DATE/iplay_game_compatibility_model_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_game_compatibility_fingerprint > $path/$DATE/iplay_game_compatibility_fingerprint_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_editor_info > $path/$DATE/iplay_editor_info_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_tags_category_id > $path/$DATE/iplay_tags_category_id_$DATE.sql
#mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_test_imei > $path/$DATE/iplay_test_imei_$DATE.sql
#mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_testers > $path/$DATE/iplay_testers_$DATE.sql
mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_ad_info > $path/$DATE/iplay_ad_info_$DATE.sql


echo $TIME',Bash shell: get labels and pkgs from 178'

cd $path
python get_178_labels_and_pkgs.py $path

echo $TIME',Bash shell: tar data'

tar -zcvf $DATE.tar.gz $DATE

echo $TIME',Bash shell: scp data.tar.gz from 178 to 52'

scp -r $DATE.tar.gz mgmt@116.255.129.52:/home/mgmt/update_52_iplay_data

cd $path
rm -rf  $DATE.tar.gz
rm -rf  $DATE
