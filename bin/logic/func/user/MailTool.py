from xpinyin import Pinyin
import random
suffix = ['@gmail.com', '@yahoo.com', '@msn.com', '@hotmail.com', '@aol.com', '@ask.com', '@live.com',
          '@qq.com', '@0355.net', '@163.com', '@163.net', '@263.net', '@3721.net', '@yeah.net', '@googlemail.com',
          '@mail.com', '@hotmail.com', '@msn.com', '@yahoo.com', '@gmail.com', '@aim.com', '@aol.com', '@mail.com',
          '@walla.com', '@inbox.com', '@126.com', '@163.com', '@sina.com', '@21cn.com', '@sohu.com', '@yahoo.com',
          '.cn', '@tom.com', '@qq.com', '@etang.com', '@eyou.com', '@56.com', '@x.cn', '@chinaren.com', '@sogou.com',
          '@citiz.com', '@126.com', '@163.com', '@sina.com', '@21cn.com', '@sohu.com', '@yahoo.comcn', '@tom.com',
          '@qq.com', '@etang.com', '@eyou.com', '@56.com', '@x.cn', '@chinaren.com', '@sogou.com', '@citiz.com']


class MailTool(object):
    def __init__(self):
        pass

    def gen_mail(self, name):
        str = ''
        for n in name:
            str += Pinyin().get_pinyin(n)[:1]
        return str + random.choice(suffix)

def getInstance():
    return MailTool()
