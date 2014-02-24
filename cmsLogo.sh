
#
# Little script displaying a CMS Ascii logo
# with additional infos about the machine
#

case $- in *i*)
    MACHINE_NAME=`hostname -a`
    N_USERS=`who | awk '{ print $1 }' | sort | uniq | wc -l`
    CPU_USAGE=`top -n1 -b | tail -n +8 | awk '{print $9}' | tr "\n" "+" | sed 's|++|\n|g' | bc`

    echo " "
    echo "    _________________________________ "
    echo "   | ‾⁻⁻--..__                       |"
    echo "   |          \`⁻-._                  |"
    echo "   |   ₃C³³³C M    \`M  ₃³³₃          |"
    echo "   |  ₃C      M₂   ₂M  S₃       /    |"
    echo "   |  ₃C      M M M M    ³S   .\"     |       [ Welcome to ${MACHINE_NAME} ]       "
    echo "   |   ³C₃₃₃C M  *  M₂ ³₃₃³_×\`       |                                            "
    echo "   |__                   ,-  \`.      |        > $N_USERS users logged in          "
    echo "   |  ‾‾\`⁻-._          ,\"      \.\"   |     > Current CPU usage : ${CPU_USAGE}% " 
    echo "   |         ‾-.   _.-‾      _,\"\    |                                            "
    echo "   |            \`×\"¨      _,⁻    \   |"
    echo "   |⁻⁻--._   _,-‾ \`,_..-⁻‾     /  ;  |"
    echo "   |      ‾×, _,-‾‾ \       _,\"    ; |"
    echo "   |--._ ,\`.·\`\      \__,,-⁻       ; |"
    echo "   |   ,'×_.-\`\`\‾‾‾‾‾‾;       ,     ;|"
    echo "   |_ //-_,----.\.__  ;    _,-       |"
    echo "   |_/×\`‾   \    ;  ‾‾‾;‾‾\`          |"
    echo "   |*)_)____;____;_____;_____________|"
    echo ""
esac


