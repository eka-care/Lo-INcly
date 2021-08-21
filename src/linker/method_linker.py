

class MethodLinker():
    def __init__(self, model):
        self.model = model
    
    def resolve(self, method, search_space, threshold=0.8):
        search_space["method_matched"] = search_space.METHOD_TYP.apply(lambda x: 1 if x == method else 0)
        search_space.sort_values("method_matched", ascending=False, inplace=True)
        return search_space.LOINC_NUM.tolist()
