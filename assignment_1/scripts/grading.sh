echo '####################'
echo '#  Grading Script  #'
echo '####################'
echo

scoring=true
python morphology.py Dict0.txt Rules0.txt Test0.txt > yourTrace.txt

if $scoring; then
    missing=$( comm -13 <(sed '/^$/d' yourTrace.txt | sort ) \
                        <(sed '/^$/d' Trace0.txt | sort ) | wc -l )
    extra=$( comm -23 <(sed '/^$/d' yourTrace.txt | sort ) \
                      <(sed '/^$/d' Trace0.txt | sort ) | wc -l )
    t1=$( sed '/^$/d' Trace0.txt | wc -l )
    t2=$( sed '/^$/d' yourTrace.txt | wc -l )
    echo "Missing Derivations:" $missing
    echo "Extra Derivations:" $extra
    if [[ $missing -eq "0" && $extra -eq "0" ]]; then
        echo "Correct!"
    fi
else
    ds=$( diff -y yourTrace.txt Trace0.txt )
    if [ -z "$ds" ]; then
        echo "Correct!"
    else
        echo "There are some errors!"
        diff -y yourTrace.txt Trace0.txt
    fi
fi
