
class TestNameLinker():
    def __init__(self, model):
        self.model = model

    def preprocess_word(self, word):
        word = str(word).lower()
        word = " ".join(word.strip().split())
        return word

    def get_similarity_score(self, word_1, word_2):
        word_1 = self.preprocess_word(word_1)
        word_2 = self.preprocess_word(word_2)
        score = self.model.wv.similarity(word_1, word_2)
        return score

    def resolve_by_semantic_similarity(self, test_name, search_space, similarity_threshold=0.8):
        candidates = {}
        for _, row in search_space.iterrows():
            score_component = self.get_similarity_score(row.COMPONENT, test_name)
            score_lcn = self.get_similarity_score(row.LONG_COMMON_NAME, test_name)
            score_sn = self.get_similarity_score(row.SHORTNAME, test_name)
            score = max(score_component, score_lcn, score_sn)
            if score > similarity_threshold:
                candidates[row.LOINC_NUM] = score

        sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)

        result_loincs = [loinc for loinc, score in sorted_candidates]
        return result_loincs

    def resolve(self, test_name, search_space, similarity_threshold=0.8):
        candidates_by_semantic_similarity = self.resolve_by_semantic_similarity(test_name, search_space, similarity_threshold)
        return candidates_by_semantic_similarity
