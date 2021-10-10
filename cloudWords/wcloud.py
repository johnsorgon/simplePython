
import string
import random
import re
# Functions adapted from ProgrammingHistorian
# http://niche.uwo.ca/programming-historian/index.php/Tag_clouds


def make_HTML_word(word, cnt, high, low):
    '''
    Make a word with a font size and a random color.
    Font size is scaled between html_big and html_little (to be user set).
    high and low represent the high and low counts in the document.
    cnt is the count of the word. 
    Required -- word (string) to be formatted
             -- cnt (int) count of occurrences of word
             -- high (int) highest word count in the document
             -- low (int) lowest word count in the document
    Return -- a string formatted for HTML that is scaled with respect to cnt
    '''
    html_big = 96
    html_little = 14
    if high != low:
        ratio = (cnt-low)/float(high-low)
    else:
        ratio = 0
    font_size = html_big*ratio + (1-ratio)*html_little
    font_size = int(font_size)
    rgb = (random.randint(0, 255), random.randint(
        0, 255), random.randint(0, 255))
    word_str = '<span style=\"color: rgb{}; font-size:{:s}px;\">{:s}</span>'
    return word_str.format(rgb, str(font_size), word)


def make_HTML_box(body):
    '''
    Take one long string of words and put them in an HTML box.
    If desired, width, background color & border can be changed in the function
    This function stuffs the "body" string into the the HTML formatting string.

    Required -- body (string), a string of words
    Return -- a string that specifies an HTML box containing the body
    '''
    box_str = """<div style=\"
    width: 560px;
    background-color: rgb(250,250,250);
    border: 1px grey solid;
    text-align: center\" >{:s}</div>
    """
    return box_str.format(body)


def print_HTML_file(body, title):
    '''
    Create a standard html page (file) with titles, header etc.
    and add the body (an html box) to that page. File created is title+'.html'
    Required -- body (string), a string that specifies an HTML box
    Return -- nothing
    '''
    fd = open(title+'.html', 'w')
    the_str = """
    <html> <head>
    <title>"""+title+"""</title>
    </head>

    <body>
    <h1>"""+title+'</h1>'+'\n'+body+'\n'+"""<hr>
    </body> </html>
    """
    fd.write(the_str)
    fd.close()

# additional method
# proses_sw for processing list of word that will be compared with stopwords
# then if the stopwords in the list of word, it will be removed

def proses_sw(listkata,stopwords):
# initialize list for listkata as "k" and stopwords as "s"
    k = []
    s = []
# initialize dictionary
    counter = {}
#the process of looping each word and adding it to the declared list
    for l_kata in listkata:
        k.append(l_kata)
    for l_stop in stopwords:
        s.append(l_stop)
# declare new list from compared stopwords and listkata
    new = [baru for baru in k if baru not in s]

#count each word also add word and count into dictionary as key and value
    for letter in new:
        if letter not in counter:
            counter[letter] = 0
        counter[letter] += 1
# convert dictionary into a list of tuples, sort by descending values
    p1 = sorted(counter.items(), key=lambda x:x[1], reverse = True)
# get top 56 
    p = p1[:56]
# re-convert list into dictionary to sort items by ascending keys / by alphabet
    res_p = dict((x,y) for x,y in p)
    result = sorted(res_p.items(), key=lambda x:x[0], reverse = False)
    return result

def print_out_result(daftar):
# convert lists to sort descending values from the top 56 of lists
    d = dict((x,y) for x,y in daftar)
    temp = sorted(d.items(), key=lambda x:x[1], reverse = True)
    for key,val in enumerate(temp):
        index1 = val[0]
        index2 = val[1]
        # print a list of tuples in the form of 4 rows and 14 columns 
        if (key+1)%4 ==0 and key!=0 :
            print('{:>2}:{:<14}'.format(str(index2), str(index1)))
        else:
            print('{:>2}:{:<14}'.format(str(index2), str(index1)), end = " ")

def main():
    print('''Program untuk membuat word cloud dari text file
---------------------------------------------
hasilnya disimpan sebagai file html,
yang bisa ditampilkan di browser.\n\n''')
    filenya = str(input("Silakan masukan nama file: "))
    filestop = "stopwords.txt"
    # read file from input    
    bl = open(filenya,"r")
    baca = bl.read().lower()

    #read stopword
    sl = open(filestop,"r")
    stopweord = sl.read().lower()

    # remove string punctuation
    exc = string.punctuation + string.digits
    table_ = str.maketrans("","",exc)
    teks = baca.translate(table_)
    # remove special chars excluded from str punctuation
    rmdash = re.sub('\â€“','',teks)
    split_kata = re.split("\s|(?<!\d)[,.](?!\d)",rmdash)
    
    srep = stopweord.split('\n')
    
    # filter empty string in split_kata
    list_kata = list(filter(None,split_kata))
    list_stop = list(filter(None,srep))

    # take list of word & stopword using proses_sw function
    paired = proses_sw(list_kata,list_stop)
    
#    pairs = [('bogor', 25), ('depok', 6), ('medan', 41),
#             ('jakarta', 19), ('bandung', 30)]
    high_count = 20
    low_count = 2
    body = ''
    for word, cnt in paired:
        body = body + " " + make_HTML_word(word, cnt, high_count, low_count)
    box = make_HTML_box(body)  # creates HTML in a box
    # writes HTML to file name 'testFile.html'
    print_HTML_file(box, filenya)

    print(filenya," :\n56 kata diurutkan berdasarkan jumlah kemunculan dalam pasangan\njumlah:kata)\n")
    # print_out result of word count from descending 
    print_out_result(paired)

    input("Tekan Enter untuk keluar...")
if __name__ == '__main__':
    main()
