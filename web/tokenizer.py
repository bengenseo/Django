import jieba
from whoosh.analysis import Token, Tokenizer


class ChineseTokenizer(Tokenizer):
    def __call__(self, value, positions=False, chars=False, keepalive=False, removestops=True, start_pos=0,start_char=0, mode='', **kwargs):
        if mode=='query':
            keys = Token(positions, chars, removestops=removestops, mode=mode, **kwargs)
            seglist = jieba.cut(value, cut_all=False)
            for w in seglist:
                # print(w)
                keys.original = keys.text = w
                keys.boost = 1.0
                if positions:
                    keys.pos = start_pos + value.find(w)
                if chars:
                    keys.startchar = start_char + value.find(w)
                    keys.endchar = start_char + value.find(w) + len(w)
                yield keys


def ChineseAnalyzer():
    return ChineseTokenizer()
