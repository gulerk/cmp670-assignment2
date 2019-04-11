from collections import OrderedDict
import random

class CFG(OrderedDict):
    def __init__(self, *args):
        super().__init__(map(lambda s: s.replace(' ', '').split('->'), args))
        
    def __repr__(self):
        return '\n'.join('{} -> {}'.format(k, v) for k, v in self.items())

    def getProductions(self, symbol):
        return self[symbol].split('|')

# Depth-first walk through tree, selecting random productions
def generateSentence(cfg, start='S'):
    string = []
    def dfs(root):
        local_str = ''
        prod = random.choice(cfg.getProductions(root))
        for char in prod:
            if char in cfg:
                result = dfs(char)
                if result:
                    string.append(result)
            else:
                local_str += char
        return local_str

    dfs(start)
    return ' '.join(string[:-1]).capitalize() + string[-1]

if __name__ == "__main__":
    # Example CFG found online
    L = [
        'S -> NP VP',
        'PP -> P NP',
        'VP -> V NP | VP PP',
        'NP-> NP PP | "astronomers" | "ears" | "telescope" | "stars"',
        'P -> "with"',
        'V -> "saw"'
    ]

    # Replacing variable names for simpler parsing
    table = OrderedDict([
        ('NP',       'A'),
        ('VP',       'B'),
        ('PP',       'C'),
        ('P',        'D'),
        ('V',        'E')
    ])

    for i in range(len(L)):
        L[i] = L[i].replace('\"', '')
        for key in table:
            L[i] = L[i].replace(key, table[key])

    cfg = CFG(*L)
	
    f = open("random-sentence.txt","w+")
	
    for i in range(10):
     sentence = generateSentence(cfg)
     f.write("%s\r\n" % sentence)
     print(sentence)