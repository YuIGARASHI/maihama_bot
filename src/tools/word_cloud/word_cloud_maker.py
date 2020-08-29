from PIL import Image
import numpy as np
import wordcloud, codecs
import MeCab

title = "君はともだち"
file = codecs.open('texts/' + title + '.txt','r', 'utf-8', 'ignore')
text = file.read()
msk = np.array(Image.open('images/mickey-circle.jpg'))

m = MeCab.Tagger("")
text = text.replace('\r','')
parsed = m.parse(text)

#助詞、助動詞を除いて単語結合
splitted = ' '.join([x.split('\t')[0] for x in parsed.splitlines()[:-1] if x.split('\t')[1].split(',')[0] not in ['助詞', '助動詞']])

wordc = wordcloud.WordCloud(font_path='HGRGM.TTC',
        background_color='white',
        mask=msk,
        contour_color='steelblue',
        contour_width=0).generate(splitted)

wordc.to_file('output/' + title + '.png')