BEGIN {printf("%s\t%s\n", "COUNT", "USER")}

NR > 1 {num[$1]++}

END {
        for (i in num)
                    print num[i] "\t" i | "sort -r -n"
}
