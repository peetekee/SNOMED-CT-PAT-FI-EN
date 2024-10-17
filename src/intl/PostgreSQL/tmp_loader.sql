/* Generated Loader Script */

set schema 'snomedct';

\copy concept_f from '/Users/matiastolppanen/healthcare/snomed_ct/thl/SNOMED-CT-PAT-FI-EN/src/intl/PostgreSQL/tmp_extracted/sct2_Concept_Full_INT_20240901.txt' WITH (FORMAT csv, HEADER true, DELIMITER E'\t', QUOTE E'\b');
\copy description_f from '/Users/matiastolppanen/healthcare/snomed_ct/thl/SNOMED-CT-PAT-FI-EN/src/intl/PostgreSQL/tmp_extracted/sct2_Description_Full-en_INT_20240901.txt' WITH (FORMAT csv, HEADER true, DELIMITER E'\t', QUOTE E'\b');
\copy stated_relationship_f from '/Users/matiastolppanen/healthcare/snomed_ct/thl/SNOMED-CT-PAT-FI-EN/src/intl/PostgreSQL/tmp_extracted/sct2_StatedRelationship_Full_INT_20240901.txt' WITH (FORMAT csv, HEADER true, DELIMITER E'\t', QUOTE E'\b');
\copy relationship_f from '/Users/matiastolppanen/healthcare/snomed_ct/thl/SNOMED-CT-PAT-FI-EN/src/intl/PostgreSQL/tmp_extracted/sct2_Relationship_Full_INT_20240901.txt' WITH (FORMAT csv, HEADER true, DELIMITER E'\t', QUOTE E'\b');
\copy textdefinition_f from '/Users/matiastolppanen/healthcare/snomed_ct/thl/SNOMED-CT-PAT-FI-EN/src/intl/PostgreSQL/tmp_extracted/sct2_TextDefinition_Full-en_INT_20240901.txt' WITH (FORMAT csv, HEADER true, DELIMITER E'\t', QUOTE E'\b');
\copy attributevaluerefset_f from '/Users/matiastolppanen/healthcare/snomed_ct/thl/SNOMED-CT-PAT-FI-EN/src/intl/PostgreSQL/tmp_extracted/der2_cRefset_AttributeValueFull_INT_20240901.txt' WITH (FORMAT csv, HEADER true, DELIMITER E'\t', QUOTE E'\b');
\copy langrefset_f from '/Users/matiastolppanen/healthcare/snomed_ct/thl/SNOMED-CT-PAT-FI-EN/src/intl/PostgreSQL/tmp_extracted/der2_cRefset_LanguageFull-en_INT_20240901.txt' WITH (FORMAT csv, HEADER true, DELIMITER E'\t', QUOTE E'\b');
\copy associationrefset_f from '/Users/matiastolppanen/healthcare/snomed_ct/thl/SNOMED-CT-PAT-FI-EN/src/intl/PostgreSQL/tmp_extracted/der2_cRefset_AssociationFull_INT_20240901.txt' WITH (FORMAT csv, HEADER true, DELIMITER E'\t', QUOTE E'\b');
