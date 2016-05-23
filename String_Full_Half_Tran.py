# coding=utf-8
# 使python可以讀取中文

# 全型轉半型# 
def strF2H(ustring):
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code==0x3000:
            inside_code=0x0020
        else:
            inside_code-=0xfee0
        if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
            rstring += uchar
        rstring += unichr(inside_code)
    return rstring

# 半型轉全型
def strH2F(ustring):
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
            rstring += uchar
        if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
            inside_code=0x3000
        else:
            inside_code+=0xfee0
        rstring += unichr(inside_code)
    return rstring




a = strH2F("abc12345")
print a
b = strF2H(a)
print b
