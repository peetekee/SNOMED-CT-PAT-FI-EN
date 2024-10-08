import pandas as pd
from services import Database, Get, Excel
from config import Config



class CompareIntl:
    def __init__(self, password, start, end) -> None:
        self.__conf = Config(password)
        self.__excel = Excel(self.__conf)
        self.__database = Database(self.__conf)
        self.__start = start
        self.__end = end

    def run(self, progress_callback=None):
        if progress_callback:
            progress_callback(5)
        thl_sct_pat = self.__database.get()
        thl_sct_pat = Get.en_row(thl_sct_pat)
        intl_tables = self.__database.get_intl()
        if progress_callback:
            progress_callback(10)
        snap_concept = intl_tables["snap_concept"]
        snap_concept['effectivetime'] = pd.to_datetime(snap_concept['effectivetime'], format='%Y%m%d')
        snap_concept = snap_concept[(snap_concept['effectivetime'] >= self.__start) & (snap_concept['effectivetime'] <= self.__end)]

        snap_attributevaluerefset = intl_tables["snap_attributevaluerefset"]

        snap_associationrefset = intl_tables["snap_associationrefset"]

        snap_pref = intl_tables["snap_pref"]

        snap_fsn = intl_tables["snap_fsn"]
        snap_fsn['effectivetime'] = pd.to_datetime(snap_fsn['effectivetime'], format='%Y%m%d')
        snap_fsn = snap_fsn[(snap_fsn['effectivetime'] >= self.__start) & (snap_fsn['effectivetime'] <= self.__end)]

       # Create inactive_conceptid equivalent
        if progress_callback:
            progress_callback(20)

        inactive_conceptid = thl_sct_pat[thl_sct_pat['A:Active'] == 'Y'].merge(
            snap_concept[snap_concept['active'] == '0'],
            left_on='A:SNOMEDCT',
            right_on='id',
            how='inner'
        )
        
        # Taking the relevant columns
        inactive_conceptid = inactive_conceptid[["CodeId", "A:Active", "A:SNOMEDCT", "A:SCT_Concept_FSN", "effectivetime", "active"]]

        # Get inactivations reason ids
        reason = inactive_conceptid.merge(
            snap_attributevaluerefset[["referencedcomponentid", "valueid"]],
            left_on='A:SNOMEDCT',
            right_on='referencedcomponentid',
            how='left'
        )

        # Get names for inactivations reason ids
        reason = reason.merge(
            snap_pref[["conceptid", "term"]],
            left_on='valueid',
            right_on='conceptid',
            how='left'
        )

        #clean up
        reason = reason[["CodeId", "A:SNOMEDCT", "term"]]

        if progress_callback:
            progress_callback(40)

        # Function to create association tables (replaced_by, same_as, alternative, etc.)
        def create_association_table(row):
            # get orginal row
            original_row = thl_sct_pat[thl_sct_pat["CodeId"] == row["CodeId"]].copy()
            # set reason for inactivation
            inactivation_reason = reason[reason["CodeId"] == row["CodeId"]]["term"].values[0]
            original_row["Meta"] = inactivation_reason
            # Get the replacement suggestion if any.
            associations_df = snap_associationrefset[snap_associationrefset['referencedcomponentid'] == row["A:SNOMEDCT"]]
            if not associations_df.empty:
                # Get association name
                associations_df = associations_df.merge(
                    snap_pref[["conceptid", "term"]],
                    left_on='refsetid',
                    right_on='conceptid',
                    how='left'
                ).rename(columns={"term":"Association_Type"})

                # Get target concept fsn and pref
                associations_df = associations_df.merge(
                    snap_fsn[["conceptid", "term"]],
                    left_on='targetcomponentid',
                    right_on='conceptid',
                    how='left'
                ).rename(columns={"term":"A:SCT_Concept_FSN"})


                # Problems with US - GB pref
                # associations_df = associations_df.merge(
                #     snap_pref[["conceptid", "term"]],
                #     left_on='targetcomponentid',
                #     right_on='conceptid',
                #     how='left'
                # ).rename(columns={"term":"LongName"})

                associations_df = associations_df[['targetcomponentid', 'Association_Type', 'A:SCT_Concept_FSN']]
                result = original_row
                for index, replacement_row in associations_df.iterrows():
                    new_row = original_row.copy()
                    new_row["status"] = "new_concept"
                    legacy, sct_id = Get.legacyid(new_row["A:Legacy_ConceptID"].values[0])
                    new_id = f"{legacy}-{replacement_row['targetcomponentid']}"
                    new_row["A:Legacy_ConceptID"] = new_id
                    new_row["A:Legacy_TermID"] = f"{legacy}-"
                    new_row["A:SCT_TermID"] = ""
                    new_row["LongName"] = ""
                    new_row["A:SNOMEDCT"] = replacement_row["targetcomponentid"]
                    new_row["A:SCT_Concept_FSN"] = replacement_row["A:SCT_Concept_FSN"]
                    new_row["Meta"] = replacement_row["Association_Type"]
                    result = pd.concat([result, new_row])          
                return result
        
        def create_fsn_updates():
            fi_fsn_intl_fsn = thl_sct_pat.merge(
                snap_fsn[["conceptid", "term"]],
                left_on='A:SNOMEDCT',
                right_on='conceptid',
                how='inner'
            )

            rows_with_different_values = fi_fsn_intl_fsn[fi_fsn_intl_fsn["A:SCT_Concept_FSN"] != fi_fsn_intl_fsn["term"]]

            product = None
            if not rows_with_different_values.empty:
                counter = 1
                for i, row in rows_with_different_values.iterrows():
                    row["Meta"] = ""
                    row.reset_index(drop=True)
                    new_row = row.copy()
                    new_row["status"] = "fsn"
                    new_row["Meta"] = "New FSN"
                    new_row["A:SCT_Concept_FSN"] = row["term"]
                    new_row.reset_index(drop=True)
                    if counter == 1:
                        product = pd.DataFrame([row])
                        product = pd.concat([product, pd.DataFrame([new_row])])
                        counter += 1
                    else:
                        product = pd.concat([product, pd.DataFrame([row])])
                        product = pd.concat([product, pd.DataFrame([new_row])])
                return product

        collection = []
        for index, row in inactive_conceptid.iterrows():
            result = create_association_table(row)
            collection.append(result)
        if progress_callback:
            progress_callback(75)
        final = pd.concat(collection)
        fsn_result = create_fsn_updates()
        fsn_result = fsn_result.drop(['conceptid', 'term'], axis=1)
        final = pd.concat([final, fsn_result])
        if progress_callback:
            progress_callback(100)
        self.__excel.post_intl_comparison(final)
