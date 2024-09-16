import pandas as pd
from services import Database
from config import Config

password = ""
conf = Config(password)

database = Database(conf)
intl_tables = database.get_intl()
# Dataframes: thl_sct_pat, snap_concept, snap_attributevaluerefset, snap_associationrefset, snap_fsn

# Inactive ConceptID Subquery
inactive_conceptid = thl_sct_pat.merge(snap_concept, left_on='A:SNOMEDCT', right_on='id', how='left')
inactive_conceptid = inactive_conceptid[(inactive_conceptid['A:Active'] == 'Y') & (inactive_conceptid['active'] == '0')]
inactive_conceptid = inactive_conceptid[['codeid', 'A:Active', 'A:Lang', 'A:Legacy_ConceptID', 'A:SNOMEDCT', 'A:SCT_Concept_FSN']]

# Reason Subquery
reason = inactive_conceptid.merge(snap_attributevaluerefset, left_on='A:SNOMEDCT', right_on='referencedcomponentid', how='left')
reason['reason_for_inactivation'] = reason['valueid'].map({
    '900000000000482003': 'Duplicate',
    '900000000000483008': 'Outdated',
    '900000000000484002': 'Ambiguous',
    '900000000000485001': 'Erroneous',
    '900000000000486000': 'Limited',
    '900000000000487009': 'Moved elsewhere',
    '900000000000492006': 'Pending move',
    '1186917008': 'Classification derived',
    '1186919006': 'Unknown meaning',
    '723277005': 'Nonconformance to editorial policy'
}).fillna('Unknown')
reason = reason[reason['active'] == '1'][['codeid', 'reason_for_inactivation']]

# Function to handle different replacement types
def get_replacement(ic, refsetid, association_name):
    replacement = ic.merge(snap_associationrefset, left_on='A:SNOMEDCT', right_on='referencedcomponentid', how='left')
    replacement = replacement[(replacement['refsetid'] == refsetid) & (replacement['active'] == '1')]
    replacement['association'] = association_name
    return replacement[['codeid', 'association', 'targetcomponentid']]

# Replacement subqueries
replaced_by = get_replacement(inactive_conceptid, '900000000000526001', 'Replaced by')
same_as = get_replacement(inactive_conceptid, '900000000000527005', 'Same as')
alternative = get_replacement(inactive_conceptid, '900000000000530003', 'Alternative')
possibly_replaced_by = get_replacement(inactive_conceptid, '1186921001', 'Possibly replaced by')
possibly_equivalent_to = get_replacement(inactive_conceptid, '900000000000523009', 'Possibly equivalent to')
partially_equivalent_to = get_replacement(inactive_conceptid, '1186924009', 'Partially equivalent to')

# Union all the replacements
all_replacements = pd.concat([replaced_by, same_as, alternative, possibly_replaced_by, possibly_equivalent_to, partially_equivalent_to])

# Final query
final = inactive_conceptid.merge(reason, on='codeid', how='left')
final = final.merge(all_replacements, on='codeid', how='left')
final = final.merge(snap_fsn, left_on='targetcomponentid', right_on='conceptid', how='left')
final = final.merge(snap_concept, left_on='conceptid', right_on='id', how='left')

# Filter by date range and language
final['effectivetime'] = pd.to_datetime(final['effectivetime'], format='%Y%m%d')
final = final[(final['effectivetime'] >= '2023-10-01') & (final['effectivetime'] <= '2024-01-02')]
final = final[final['A:Lang'] == 'en']

# Select columns
final_result = final[['codeid', 'reason_for_inactivation', 'association', 'targetcomponentid', 'term', 'active', 'effectivetime']]

# Display result
import ace_tools as tools; tools.display_dataframe_to_user(name="Final Result", dataframe=final_result)

