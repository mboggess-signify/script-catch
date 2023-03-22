#!/bin/zsh

policies_file="nr-policies-2.txt"
#policies_file="nr-policies-small-test.txt"
notifications_file="nr-channels-with-policies-stripped.json"
output_file="policy-channel.json"

#echo "Policies file is $policies_file"
#echo "Notifications file is $notifications_file"
#echo "Output file is $output_file"
#
#ls -l $policies_file
#ls -l $notifications_file
#ls -l $output_file
#
first_line=$(head -n 1 $policies_file)
last_line=$(tail -n 1 $policies_file)
declare -a channels_array

while read p_lines;
do
  echo "Looking for policy ID: $p_lines"
  # Build array of notification channels assigned to $p_lines policy
  channels_array=(`jq -j "[.channels[] | select(.associatedPolicies.policies[].id == \"$p_lines\") |{name:.name,id:.id}]" $notifications_file | gsed -e 's/ //g'`)
    #gsed -e 's/\[//g' -e 's/\]//g' -e 's/\,//g' -e 's/"//g' -e 's/ //g' | \
    #tr '\n' ' '`)
  #echo ${channels_array[*]}
  #sleep 5

  # Grab policy name
  #echo $p_lines
  policy_name=`jq ".channels[].associatedPolicies.policies[] | select(.id == \"$p_lines\") | .name" $notifications_file | head -n 1`
  #echo $policy_name
  #sleep 10

  # Build json output file for `jsoncsv` translation
  echo "{\"policy_name\":$policy_name,\"policy_id\":\"$p_lines\",\"notification_channels\":${channels_array[*]}}" >> policy-channel-to-csv.json

  # Build json output file for jq/well-formed
  #if [ "$p_lines" = "$first_line" ];
  #then
  #  echo "{
  #\"information\": [
  #  {
  #    \"policy_name\": $policy_name,
  #    \"policy_id\": \"$p_lines\",
  #    \"notification_channels\": ${channels_array[*]}
  #  }," >> policy-channel.json
  #elif [ "$p_lines" = "$last_line" ];
  #then
  #  echo "    {
  #    \"policy_name\": $policy_name,
  #    \"policy_id\": \"$p_lines\",
  #    \"notification_channels\": ${channels_array[*]}
  #  }
  #]
#}" >> policy-channel.json
#  else
#    echo "    {
#      \"policy_name\": $policy_name,
#      \"policy_id\": \"$p_lines\",
#      \"notification_channels\": ${channels_array[*]}
#    }," >> policy-channel.json
#  fi
done < $policies_file
