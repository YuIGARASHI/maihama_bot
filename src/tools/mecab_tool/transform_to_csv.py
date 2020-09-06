import codecs

if __name__ == "__main__":
    ifs = codecs.open("../../../static_data/word_data.txt", "r", "utf-8")
    ofs = codecs.open("../../../tmp/disney-dic.csv", "w", "utf-8")
    words = ifs.read()

    # 語の重複を削除
    word_set = set()
    for word in words.splitlines():
        word_set.add(word.strip())
    
    # ソート
    word_list = list(word_set)
    word_list.sort()

    for word in word_list:
        # 読み仮名は全部適当に...
        output_str = (word + ",,,1,名詞,固有名詞,一般,*,*,*,self-add,self-add,self-add")
        ofs.write(output_str + "\n")
    
    ifs.close()
    ofs.close()

    # 元データも重複削除 & ソート
    ofs = codecs.open("../../../static_data/word_data.txt", "w", "utf-8")
    for word in word_list:
        ofs.write(word + "\n")