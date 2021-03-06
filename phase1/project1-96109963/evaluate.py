import glob
from helper import Eval_calc, mean, Text_cleaner
from index_construction import RetrievalIndex
class IREvaluator:

    funcs = {'F': Eval_calc.F,
            'MAP': Eval_calc.MAP,
            'R': Eval_calc.R_precision,
            'NDCG': Eval_calc.NDCG,
            }

    def __init__(self, retrieval_index=None,
            queries_path='./data/',
            query_nums=20):
        self.retrieval_index = retrieval_index
        self.queries_path = queries_path
        self.query_nums = query_nums

    def query_path(self, num='all'):
        return [self.queries_path + ("queries/%s.txt" % i) for i in (range(1, self.query_nums) if num == 'all' else [num])]

    def result_path(self, num='all'):
        return [self.queries_path + ("relevance/%s.txt" % i) for i in (range(1, self.query_nums) if num == 'all' else [num])]

    def q_and_res_path(self, num='all'):
        return zip(self.query_path(num), self.result_path(num))

    def evaluate(self, query_id='all', metric='F', method='ltn-lnn', verbose=False):
        should_divide = (method[2] == 'c')
        scores = []
        for i, (q, res) in enumerate(self.q_and_res_path(query_id)):
            with open(q, 'r') as f:
                lines = f.read().split('\n')
                if len(lines) < 1:
                    raise ValueError('file has no lines')
                query_title = lines[0]
                if len(lines) > 1 and len(lines[1].replace(' ', '')) > 0:
                    query_text = lines[1]
                else:
                    query_text = query_title
#                if verbose:
#                    print("Query title: %s, query text: %s" % (query_title, query_text))
#                    print('\n'.join(map(str, Text_cleaner.query_cleaner(query_title))))
                top_k = self.retrieval_index.query(query_title, query_text, should_divide)

            with open(res, 'r') as f:
                real_best = f.read().replace(',', '').split()

            scores.append(IREvaluator.funcs[metric](real_best, top_k))
            if verbose:
                print(top_k)
                print(query_text)
                print(query_title)
                print(real_best)
                print("i = %d, q = %s" % (i, q))
#                print("query = %s" % query_title)
                print("metric = %s, Element %.2f, runing mean = %.2f" % (metric, scores[-1], mean(scores)))
                print()
        
        assert len(scores) > 0
        return sum(scores)/ len(scores)
