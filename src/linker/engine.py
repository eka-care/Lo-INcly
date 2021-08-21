
import pandas as pd

from gensim.models import FastText

from src.linker.test_linker import TestNameLinker
from src.linker.unit_linker import UnitLinker
from src.linker.specimen_linker import SpecimenLinker
from src.linker.method_linker import MethodLinker

class Engine():
    def __init__(self):
        self.model = FastText.load("data/ft_oa_all_100d.bin")
        self.kb = pd.read_csv("data/loinc_2000_MostCommon_db.csv")
        self.kb = self.preprocessing_for_testname_linking(self.kb)

        self.test_linker = TestNameLinker(self.model)
        self.unit_linker = UnitLinker(self.model)
        self.specimen_linker = SpecimenLinker(self.model)
        self.method_linker = MethodLinker(self.model)


    def preprocessing_for_testname_linking(self, df):
        df["COMPONENT"] = df["COMPONENT"].apply(lambda x: str(x).lower())
        df["LONG_COMMON_NAME"] = df["LONG_COMMON_NAME"].apply(lambda x: str(x).lower())
        df["SHORTNAME"] = df["SHORTNAME"].apply(lambda x: str(x).lower())
        return df


    def resolve(self, test_name, unit=None, specimen=None, method=None, top_k=10):
        search_space = self.kb.copy()
        candidates_by_test_name_semantic_similarity = self.test_linker.resolve(test_name, search_space=search_space)
        search_space = search_space[search_space.LOINC_NUM.isin(candidates_by_test_name_semantic_similarity)]

        candidates_by_unit = self.unit_linker.resolve(unit, search_space)
        search_space = search_space[search_space.LOINC_NUM.isin(candidates_by_unit)]

        candidates_by_specimen = self.specimen_linker.resolve(specimen, search_space)
        search_space = search_space[search_space.LOINC_NUM.isin(candidates_by_specimen)]

        candidates_by_method = self.method_linker.resolve(method, search_space)
        search_space = search_space[search_space.LOINC_NUM.isin(candidates_by_method)]

        search_space = search_space.iloc[:top_k]

        candidates = []
        for _, row in search_space.iterrows():
            candidate = dict(
                loinc=row.LOINC_NUM,
                component=row.COMPONENT,
                property=row.PROPERTY,
                system=row.SYSTEM,
                method=row.METHOD_TYP,
            )
            candidates.append(candidate)
        return candidates
