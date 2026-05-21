#!/bin/bash
# Targeted: Asian female teachers (smiling, professional) + clean small classrooms
URLS=(
  # ASIAN FEMALE TEACHERS — Pexels
  'https://images.pexels.com/photos/5212329/pexels-photo-5212329.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8617756/pexels-photo-8617756.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8617760/pexels-photo-8617760.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8617764/pexels-photo-8617764.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8617772/pexels-photo-8617772.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8617773/pexels-photo-8617773.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8617774/pexels-photo-8617774.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8617775/pexels-photo-8617775.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8617776/pexels-photo-8617776.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8617777/pexels-photo-8617777.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8617778/pexels-photo-8617778.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/5212702/pexels-photo-5212702.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/5212720/pexels-photo-5212720.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/5212656/pexels-photo-5212656.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/5905709/pexels-photo-5905709.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/5905781/pexels-photo-5905781.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/5905746/pexels-photo-5905746.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8612968/pexels-photo-8612968.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/6929183/pexels-photo-6929183.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/6963831/pexels-photo-6963831.jpeg?auto=compress&cs=tinysrgb&w=800'
  # SMALL CLEAN CLASSROOMS (Asian preferred)
  'https://images.pexels.com/photos/5212317/pexels-photo-5212317.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/5212333/pexels-photo-5212333.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/5212344/pexels-photo-5212344.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8617743/pexels-photo-8617743.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8617758/pexels-photo-8617758.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/4144101/pexels-photo-4144101.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8617763/pexels-photo-8617763.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8617750/pexels-photo-8617750.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8617790/pexels-photo-8617790.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/6549623/pexels-photo-6549623.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/6929214/pexels-photo-6929214.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8442100/pexels-photo-8442100.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8423031/pexels-photo-8423031.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8466691/pexels-photo-8466691.jpeg?auto=compress&cs=tinysrgb&w=800'
  'https://images.pexels.com/photos/8472750/pexels-photo-8472750.jpeg?auto=compress&cs=tinysrgb&w=800'
)
for url in "${URLS[@]}"; do
  code=$(/usr/bin/curl -s -o /dev/null -w '%{http_code}' --max-time 6 "$url")
  short=$(echo "$url" | /usr/bin/sed 's|.*photos/||;s|.*photo-||;s|?.*||;s|/.*||')
  echo "$code  $short"
done
