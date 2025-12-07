#!/usr/bin/env bash
KS="/home/rahim_admin_user1/new-release-key.keystore"
candidates=(
"555555" "55555" "0555555" "5555550" "5555551" "55555500" "55555555"
"555555123" "123555555" "rahim555" "rahim555555" "evolution555"
"evolutionrun555" "vira555" "rahim123" "tajikistan555"
"000000" "111111" "123456" "12345678" "5555" "5555555" "55555555"
"mykey" "my-release" "newrelease" "new-release" "release"
)
echo "Проверяю ${#candidates[@]} вариантов для $KS ..."
for pw in "${candidates[@]}"; do
  printf "Пробую: %s ... " "$pw"
  out=$(keytool -list -v -keystore "$KS" -storepass "$pw" 2>&1)
  if echo "$out" | grep -q "Keystore type"; then
    echo "OK — пароль подошёл! (пароль: $pw)"
    echo "----- Отрывок вывода keytool:"
    echo "$out" | sed -n '1,120p' | sed 's/^/   /'
    exit 0
  else
    echo "нет"
  fi
done
echo "Ни один кандидат не подошёл."
