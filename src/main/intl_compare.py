import pandas as pd
import numpy as np
from services import Database
from config import Config



class CompareIntl:
    def __init__(self, password) -> None:
        self.__conf = Config(password)
        self.__database = Database(self.__conf)
        self.__run()

    def __run(self):
        thl_sct_pat = self.__database.get()
        thl_sct_pat = thl_sct_pat[thl_sct_pat['A:Lang'] == 'en']
        intl_tables = self.__database.get_intl()
        snap_concept = intl_tables["snap_concept"]
        snap_attributevaluerefset = intl_tables["snap_attributevaluerefset"]
        snap_associationrefset = intl_tables["snap_associationrefset"]
        snap_pref = intl_tables["snap_pref"]
        snap_fsn = intl_tables["snap_fsn"]
        #thl_sct_pat = ['CodeId', 'status', 'tmdc', 'A:Lang', 'A:Active', 'A:Legacy_ConceptID',
       #'A:Legacy_TermID', 'tays_snomed_ii', 'A:SNOMEDCT', 'A:SCT_Concept_FSN',
       #'A:SCT_TermID', 'ParentId', 'LongName', 'parent_conceptid',
       #'parent_concept_fsn', 'edit_comment', 'av_notes',
       #'A:ICD-O-3_Morfologia', 'icdo_term', 'icdo_synonyms', 'BeginningDate',
       #'ExpiringDate', 'A:KorvaavaKoodi', 'A:InaktivoinninSelite', 'sn2_code',
       #'sn2_term', 'endo', 'gastro', 'gyne', 'iho', 'hema', 'keuhko', 'nefro',
       #'neuro', 'paa_kaula', 'pedi', 'pehmyt', 'rinta', 'syto', 'uro',
       #'verenkierto_yleiset']
        # snap_concept = ['id', 'effectivetime', 'active', 'moduleid', 'definitionstatusid']
        # snap_attributevaluerefset = ['id', 'effectivetime', 'active', 'moduleid', 'refsetid', 'referencedcomponentid', 'valueid']
        # snap_associationrefset = ['id', 'effectivetime', 'active', 'moduleid', 'refsetid', 'referencedcomponentid', 'targetcomponentid']
        # snap_pref = ['id', 'effectivetime', 'active', 'moduleid', 'conceptid','languagecode', 'typeid', 'term', 'casesignificanceid']
        # snap_fsn = ['id', 'effectivetime', 'active', 'moduleid', 'conceptid', 'languagecode', 'typeid', 'term', 'casesignificanceid']

       # Create inactive_conceptid equivalent
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
        reason = reason.rename(columns={"term": "Reason for Inactivation"})
        print(reason)



        

        # add names to reasons
        inactive_conceptid = inactive_conceptid.merge(
            snap_pref,

        )

        # Create reason equivalent
        conditions = [
            (snap_attributevaluerefset['valueid'] == '900000000000482003'),
            (snap_attributevaluerefset['valueid'] == '900000000000483008'),
            (snap_attributevaluerefset['valueid'] == '900000000000484002'),
            (snap_attributevaluerefset['valueid'] == '900000000000485001'),
            (snap_attributevaluerefset['valueid'] == '900000000000486000'),
            (snap_attributevaluerefset['valueid'] == '900000000000487009'),
            (snap_attributevaluerefset['valueid'] == '900000000000492006'),
            (snap_attributevaluerefset['valueid'] == '1186917008'),
            (snap_attributevaluerefset['valueid'] == '1186919006'),
            (snap_attributevaluerefset['valueid'] == '723277005')
        ]
        reasons = ['Duplicate', 'Outdated', 'Ambiguous', 'Erroneous', 'Limited', 
                   'Moved elsewhere', 'Pending move', 'Classification derived', 
                   'Unknown meaning', 'Nonconformance to editorial policy']

        snap_attributevaluerefset['reason_for_inactivation'] = np.select(conditions, reasons, default='Unknown')

        # Merge inactive_conceptid with reason
        reason = inactive_conceptid.merge(
            snap_attributevaluerefset[snap_attributevaluerefset['active'] == '1'],
            left_on='A:SNOMEDCT',
            right_on='referencedcomponentid',
            how='left'
        )

        # Function to create association tables (replaced_by, same_as, alternative, etc.)
        def create_association_table(refsetid, association_label):
            return inactive_conceptid.merge(
                snap_associationrefset[
                    (snap_associationrefset['refsetid'] == refsetid) & 
                    (snap_associationrefset['active'] == '1')
                ],
                left_on='A:SNOMEDCT',
                right_on='referencedcomponentid',
                how='left'
            ).assign(association=association_label)

        # Create each association table
        replaced_by = create_association_table('900000000000526001', 'Replaced by')
        same_as = create_association_table('900000000000527005', 'Same as')
        alternative = create_association_table('900000000000530003', 'Alternative')
        possibly_replaced_by = create_association_table('1186921001', 'Possibly replaced by')
        partially_equivalent_to = create_association_table('1186924009', 'Partially equivalent to')
        possibly_equivalent_to = create_association_table('900000000000523009', 'Possibly equivalent to')

        # Union of all replacements (using concat)
        all_replacements = pd.concat([replaced_by, same_as, alternative, possibly_replaced_by, 
                                      partially_equivalent_to, possibly_equivalent_to])

        # Final merge with fsn and concept tables for extra details
        result = reason.merge(all_replacements, on='codeid', how='left') \
                       .merge(snap_fsn, left_on='new_conceptid', right_on='conceptid', how='left') \
                       .merge(snap_concept, left_on='conceptid', right_on='id', how='left')

        # Filter by effective time and language
        final_result = result[(pd.to_datetime(result['effectivetime'], format='%Y%m%d').between('2023-10-01', '2024-01-02')) & 
                              (result['A:Lang'] == 'en')]

        # Output or further processing
        import ace_tools as tools; tools.display_dataframe_to_user(name="Final Replacement Data", dataframe=final_result)
        






# # Function to handle different replacement types
# def get_replacement(ic, refsetid, association_name):
#     replacement = ic.merge(snap_associationrefset, left_on='A:SNOMEDCT', right_on='referencedcomponentid', how='left')
#     replacement = replacement[(replacement['refsetid'] == refsetid) & (replacement['active'] == '1')]
#     replacement['association'] = association_name
#     return replacement[['codeid', 'association', 'targetcomponentid']]

# # Replacement subqueries
# replaced_by = get_replacement(inactive_conceptid, '900000000000526001', 'Replaced by')
# same_as = get_replacement(inactive_conceptid, '900000000000527005', 'Same as')
# alternative = get_replacement(inactive_conceptid, '900000000000530003', 'Alternative')
# possibly_replaced_by = get_replacement(inactive_conceptid, '1186921001', 'Possibly replaced by')
# possibly_equivalent_to = get_replacement(inactive_conceptid, '900000000000523009', 'Possibly equivalent to')
# partially_equivalent_to = get_replacement(inactive_conceptid, '1186924009', 'Partially equivalent to')

# # Union all the replacements
# all_replacements = pd.concat([replaced_by, same_as, alternative, possibly_replaced_by, possibly_equivalent_to, partially_equivalent_to])

# # Final query
# final = inactive_conceptid.merge(reason, on='codeid', how='left')
# final = final.merge(all_replacements, on='codeid', how='left')
# final = final.merge(snap_fsn, left_on='targetcomponentid', right_on='conceptid', how='left')
# final = final.merge(snap_concept, left_on='conceptid', right_on='id', how='left')

# # Filter by date range and language
# final['effectivetime'] = pd.to_datetime(final['effectivetime'], format='%Y%m%d')
# final = final[(final['effectivetime'] >= '2023-10-01') & (final['effectivetime'] <= '2024-01-02')]
# final = final[final['A:Lang'] == 'en']

# # Select columns
# final_result = final[['codeid', 'reason_for_inactivation', 'association', 'targetcomponentid', 'term', 'active', 'effectivetime']]

# # Display result
# import ace_tools as tools; tools.display_dataframe_to_user(name="Final Result", dataframe=final_result)

