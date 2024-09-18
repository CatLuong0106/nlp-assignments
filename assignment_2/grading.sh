echo '####################'
echo '#  Grading Script  #'
echo '####################'
echo

scoring=true
python ngrams.py train1.txt test1.txt > yourTrace1.txt

if $scoring; then
    missing=$( comm -13 <(sed '/^$/d' yourTrace1.txt | sort ) \
                        <(sed '/^$/d' trace1.txt | sort ) | wc -l )
    extra=$( comm -23 <(sed '/^$/d' yourTrace1.txt | sort ) \
                      <(sed '/^$/d' trace1.txt | sort ) | wc -l )
    t1=$( sed '/^$/d' trace1.txt | wc -l )
    t2=$( sed '/^$/d' yourTrace1.txt | wc -l )
    echo "Missing Derivations:" $missing
    echo "Extra Derivations:" $extra
    if [[ $missing -eq "0" && $extra -eq "0" ]]; then
        echo "Correct!"
    fi
else
    ds=$( diff -y yourTrace1.txt trace1.txt )
    if [ -z "$ds" ]; then
        echo "Correct!"
    else
        echo "There are some errors!"
        diff -y yourTrace1.txt trace1.txt
    fi
fi
