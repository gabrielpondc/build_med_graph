import jieba
import jieba.posseg as pseg
import logging

jieba.setLogLevel(logging.INFO)

jieba.load_userdict("./data/userdict.txt")
def get_word_param(texts):
        result = pseg.cut(texts, use_paddle=True)
        # result_copy = result.copy()
        result_dict = dict(result)
        for k in result_dict.keys():
                if k in ['无','未','否认','不伴','排除','阴性','没有']:
                        result_dict[k] = 'ab'
        # a = "".join(["%s#%s" % (word, flag) for word, flag in result])
        # result = pseg.cut(texts, use_paddle=True)
        a = "".join(["%s#%s" % (key, result_dict[key]) for key in result_dict.keys()])
        return result_dict,a
