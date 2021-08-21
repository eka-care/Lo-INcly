
import pandas as pd

class UnitLinker():
    def __init__(self, model):
        self.model = model
        unt_to_prop_probabilities = pd.read_csv("data/unit_to_prop_prob.csv")
        self.unit_to_prop_prob_map = {}
        for _, row in unt_to_prop_probabilities.iterrows():
            if row.unit not in self.unit_to_prop_prob_map:
                self.unit_to_prop_prob_map[row.unit] = {}
            self.unit_to_prop_prob_map[row.unit][row.property] = row.probability

    def get_probability_for_unit_and_property(self, unit, property):
        prob = self.unit_to_prop_prob_map[unit].get(property, 0)
        return prob

    def resolve(self, unit, search_space):
        if unit not in self.unit_to_prop_prob_map:
            return search_space.LOINC_NUM.tolist()
        
        search_space["property_match_prob"] = search_space.PROPERTY.apply(lambda x: self.get_probability_for_unit_and_property(unit, x))
        search_space.sort_values("property_match_prob", ascending=False, inplace=True)
        return search_space.LOINC_NUM.tolist()
