steghide --extract -sf recurso/dorna.jpg -p "urumdorn4"
cat dorn4.txt | grep "flag" | sed 's/.*{\(.*\)}.*/\1/' | base64 --decode

