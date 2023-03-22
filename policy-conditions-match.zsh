#!/bin/zsh

policies_file="/Users/mboggess/signify/new-relic/nr-policies.txt"
#policies_file="/Users/mboggess/signify/new-relic/nr-policies-small-test.txt"
output_file="/Users/mboggess/signify/new-relic/policy-alerts.csv"
nr_api_key=$(cat ~/.tokens/new-relic.tkn)
#echo $nr_api_key

#echo "Policies file is $policies_file"
#echo "Output file is $output_file"

#ls -l $policies_file
#ls -l $output_file
#
echo "policy_id,alerts_enabled" > $output_file

# Loop through file of policy IDs
while read policy_id; do
  echo "Looking for $policy_id alert conditions"
  curl -X GET "https://api.newrelic.com/v2/alerts_conditions.json?policy_id=$policy_id" \
    -H "X-Api-Key:$nr_api_key" -i | grep name

  # Ask if policy has any alert conditions
  if [ $? -eq 0 ]; then
    echo "$policy_id,true" >> $output_file
  else
    echo "$policy_id,false" >> $output_file
  fi
done < $policies_file
