
class SpecimenLinker():
    def __init__(self, model):
        self.model = model
        self.specimen_dict = {
            "Ser": ["serum"],
            "Ser/Plas": ["serum", "plasma"],
            "Urine": ["urine"],
            "Bld": ["blood"],
            "Bld/Tiss": ["blood", "tissue"],
            "Body fld": ["body", "fluid"],
            "Tiss": ["tissue"],
            "Stool": ["stool"],
            "Plas": ["plasma"],
            "Heart": ["heart"],
            "Amnio fld": ["amino", "fluid"],
            "Bone mar": ["bone", "marrow"],
            "Saliva": ["saliva"],
            "Semen": ["semen"],
            "Urine sed": ["urine", "sediment"]
        }

    def get_candidate_specimen(self, specimen):
        specimen_words = specimen.lower().strip().split()
        candidate_specimens = set()
        for specimen_word in specimen_words:
            for specimen, specimen_keywords in self.specimen_dict.items():
                if specimen_word in specimen_keywords:
                    candidate_specimens.add(specimen)

        return list(candidate_specimens)

    def resolve(self, specimen, search_space, threshold=0.8):
        candidate_specimen = self.get_candidate_specimen(specimen)
        search_space["specimen_matched"] = search_space.SYSTEM.apply(lambda x: 1 if x in candidate_specimen else 0)
        search_space.sort_values("specimen_matched", ascending=False, inplace=True)
        return search_space.LOINC_NUM.tolist()
