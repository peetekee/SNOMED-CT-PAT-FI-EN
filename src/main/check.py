import json
from datetime import datetime
import pandas as pd
from services import Database, Excel, Verhoeff
from config import Config, COLUMNS


class Check:
    """Class for storing every check method"""

    # basic checks

    @staticmethod
    def codeid_unique(df):
        """Check if codeid is unique."""

        return df[df.duplicated(subset=[COLUMNS["code_id"]])], "Duplicate code id"

    @staticmethod
    def tmdc(df):
        """Check if tmdc is valid.

        Valid values include: A, C, D, M, T
        """

        return df[~df[COLUMNS["tmdc"]].str[0].isin(['A', 'C', 'D', 'M', 'T'])], "Invalid tmdc, must start with A, C, D, M or T"

    @staticmethod
    def lang(df):
        """Check if lang is valid.

        Valid values include: fi, sv, en
        """

        return df[~df[COLUMNS["lang"]].isin(['fi', 'sv', 'en'])], "Invalid lang, must be fi, sv or en"

    @staticmethod
    def active(df):
        """Check if active is valid.

        Valid values include: Y, N
        """

        return df[~df[COLUMNS["active"]].isin(["Y", "N"])], "Invalid active, must be Y or N"

    @staticmethod
    def legacy_concept_id(df):
        """Check if legacy concept id is technically valid.

        Starts with 6 alphanumeric characters, followed by a dash and an SCTID.
        """

        return df[~df[COLUMNS["legacy_concept_id"]].str.contains("^[\w\d]{6}-\d+$")], "Invalid legacy concept id, incorrect format"

    @staticmethod
    def legacy_term_id(df):
        """Check if legacy term id is technically valid.

        Starts with 6 alphanumeric characters, followed by a dash and an SCTID.
        """

        return df[~df[COLUMNS["legacy_term_id"]].str.contains("^[\w\d]{6}-\d+$")], "Invalid legacy term id, incorrect format"

    @staticmethod
    def concept_fsn(df):
        """Check if concept fsn is valid. 

        Includes a semantic tag.
        """

        return df[~df[COLUMNS["concept_fsn"]].str.contains(".+\(([^()]*)\)$")], "Invalid Concept fsn"

    @staticmethod
    def term(df):
        """Check term is not empty."""

        return df[df[COLUMNS["term"]].isna()], "Term is empty"

    @staticmethod
    def beginning_date(df):
        """Check if effective time is right format.

        Valid format: YYYY-MM-DD
        """

        return df[~df[COLUMNS["beginning_date"]].str.contains("^\d{4}-\d{2}-\d{2}$", na=False)], "Invalid beginning date format"

    @staticmethod
    def expiring_date(df):
        """Check if expiring date is right format.

        Valid format: YYYY-MM-DD
        """

        return df[~df[COLUMNS["expiring_date"]].str.contains("^\d{4}-\d{2}-\d{2}$", na=False)], "Invalid expiring date format"

    # @staticmethod
    # def concept_fsn_capital(df):
    #     """Check if concept fsn begins with capital letter."""

    #     return df[~df[COLUMNS["concept_fsn"]].str.contains("^[A-ZÄÖ0-9].+$")], "FSN begins with a lowercase letter"

    # @staticmethod
    # def term_capital(df):
    #     """Check if term begins with capital letter."""

    #     return df[~df[COLUMNS["term"]].str.contains("^[A-ZÄÖ0-9].+$")], "Term begins with a lowercase letter"

    # advanced checks

    @staticmethod
    def concept_id_checksum(df):
        """Check if concept id has correct checksum."""

        verhoeff = Verhoeff()
        mask = df[COLUMNS["concept_id"]].apply(verhoeff.validate)
        return df[~mask], "Invalid concept id checksum"

    @staticmethod
    def term_id_checksum(df):
        """Check if term id has correct checksum."""

        verhoeff = Verhoeff()
        mask = df[COLUMNS["term_id"]].apply(verhoeff.validate)
        return df[~mask], "Invalid term id checksum"

    @staticmethod
    def concept_id_legacy_concept_id(df):
        """Check if concept id and legacy concept ids SCTID part are the same."""

        return df[~df[COLUMNS["concept_id"]].eq(df[COLUMNS["legacy_concept_id"]].str.split("-").str[1])], "Concept id and Legacy conceptid last part not the same"

    @staticmethod
    def term_id_legacy_term_id(df):
        """Check if term id and legacy term ids SCTID part are the same."""

        return df[~df[COLUMNS["term_id"]].eq(df[COLUMNS["legacy_term_id"]].str.split("-").str[1])], "Term id and legacy term id last part not the same"

    @staticmethod
    def legacy_concept_id_legacy_term_id(df):
        """Check if legacy concept ids and legacy term ids SN2 part are the same."""

        return df[~df[COLUMNS["legacy_concept_id"]].str.split("-").str[0].eq(df[COLUMNS["legacy_term_id"]].str.split("-").str[0])], "Legacy concept id and legacy term id not the same"

    @staticmethod
    def beginning_expiring_date(df):
        """Check if effective_time is before supersededtime."""

        return df[~df[COLUMNS["beginning_date"]].le(df[COLUMNS["expiring_date"]])], "Beginning date is after expiring date"

    @staticmethod
    def expiring_date_active(df):
        """Check if active is N, then expiring date is in the past """

        return df[df[COLUMNS["active"]].eq("N") & df[COLUMNS["expiring_date"]].ge(datetime.now().strftime("%Y-%m-%d"))], "Expiring date is not in the past"

    @staticmethod
    def active_expiring_date(df):
        """Check if expiring date is in the past, then active is N"""

        return df[df[COLUMNS["expiring_date"]].lt(datetime.now().strftime("%Y-%m-%d")) & df[COLUMNS["active"]].ne("N")], "Expiring date is in the past but active is not 'N'"

    @staticmethod
    def no_overlap_concept_id(df):
        """Check if concept id is unique.

        Same concept id must have the same fsn and legacy concept id and tmdc first letter.
        """
        overlapping_rows = pd.DataFrame()
        grouped_df = df[COLUMNS["concept_id"]].unique()
        for concept_id in grouped_df:
            concept_rows = df[df[COLUMNS["concept_id"]] == concept_id]
            if len(concept_rows[COLUMNS["concept_fsn"]].unique()) > 1:
                overlapping_rows = pd.concat([overlapping_rows, concept_rows])
            elif len(concept_rows[COLUMNS["legacy_concept_id"]].unique()) > 1:
                overlapping_rows = pd.concat([overlapping_rows, concept_rows])
            elif len(concept_rows[COLUMNS["tmdc"]].str[0].unique()) > 1:
                overlapping_rows = pd.concat([overlapping_rows, concept_rows])
        return overlapping_rows, "Concept id overlap"

    @staticmethod
    def no_overlap_term_id(df):
        """Check if national term id is unique.

        Same term id must have the same term and legacy term id.
        """
        overlapping_rows = pd.DataFrame()
        grouped_df = df[COLUMNS["term_id"]].unique()
        for term_id in grouped_df:
            term_rows = df[df[COLUMNS["term_id"]] == term_id]
            if len(term_rows[COLUMNS["term"]].unique()) > 1:
                overlapping_rows = pd.concat([overlapping_rows, term_rows])
            elif len(term_rows[COLUMNS["legacy_term_id"]].unique()) > 1:
                overlapping_rows = pd.concat([overlapping_rows, term_rows])
        return overlapping_rows, "Term id overlap"

    @staticmethod
    def en_concept_id_is_linked_to_single_legacy_concept_id(df):
        """Check if concept id is linked to a single legacy concept id."""

        non_unique_rows_df = pd.DataFrame()
        grouped_df = df[COLUMNS["concept_id"]].unique()
        for concept_id in grouped_df:
            concept_rows = df[df[COLUMNS["concept_id"]] == concept_id]
            if len(concept_rows[COLUMNS["legacy_concept_id"]].unique()) > 1:
                non_unique_rows_df = pd.concat([non_unique_rows_df, concept_rows])
        return non_unique_rows_df, "Concept id is linked to multiple legacy concept ids"

    @staticmethod
    def en_term_id_is_linked_to_single_legacy_term_id(df):
        """Check if term id is linked to a single legacy term id."""

        non_unique_rows_df = pd.DataFrame()
        grouped_df = df[COLUMNS["term_id"]].unique()
        for term_id in grouped_df:
            term_rows = df[df[COLUMNS["term_id"]] == term_id]
            if len(term_rows[COLUMNS["legacy_term_id"]].unique()) > 1:
                non_unique_rows_df = pd.concat([non_unique_rows_df, term_rows])
        return non_unique_rows_df, "Term id is linked to multiple legacy term ids"

    @staticmethod
    def term_id_has_only_one_term(df):
        """Check if term id has only one term."""

        non_unique_rows_df = pd.DataFrame()
        grouped_df = df[COLUMNS["term_id"]].unique()
        for term_id in grouped_df:
            term_rows = df[df[COLUMNS["term_id"]] == term_id]
            if len(term_rows[COLUMNS["term"]].unique()) > 1:
                non_unique_rows_df = pd.concat([non_unique_rows_df, term_rows])
        return non_unique_rows_df, "Term id has multiple terms"

    # en row checks

    @staticmethod
    def get_lang_rows(df, en_row):
        """Tool for retrieving lang rows."""

        return df.loc[(df[COLUMNS["en_row_code_id"]] == en_row[COLUMNS["code_id"]]) & (df[COLUMNS["lang"]] != "en")]

    @staticmethod
    def concept_id_lang_same_as_concept_id_en(df, en_row):
        """Check concept id is same in lang rows as in en row."""

        lang_rows = Check.get_lang_rows(df, en_row)
        return lang_rows[~lang_rows[COLUMNS["concept_id"]].eq(en_row[COLUMNS["concept_id"]])], "Lang rows and en row concept id differ"

    @staticmethod
    def concept_fsn_same_for_all_concept_id(df, en_row):
        """Check concept fsn is same in lang rows as in en row."""

        concept_rows = df[df[COLUMNS["concept_id"]]
                          == en_row[COLUMNS["concept_id"]]]
        return concept_rows[~concept_rows[COLUMNS["concept_fsn"]].eq(en_row[COLUMNS["concept_fsn"]])], "Concept FSN differ"

    @staticmethod
    def term_lang_same_as_term_en(df, en_row):
        """Check that if term is same in lang rows as in en row, then term id is also the same."""

        lang_rows = Check.get_lang_rows(df, en_row)
        same_term = lang_rows.loc[lang_rows[COLUMNS["term"]]
                                  == en_row[COLUMNS["term"]]]
        if not same_term.empty:
            return same_term[same_term[COLUMNS["term_id"]] != en_row[COLUMNS["term_id"]]], "Term same in en and lang rows but different term id"
        return pd.DataFrame(), ""

    @staticmethod
    def term_id_lang_same_as_term_id_en(df, en_row):
        """Check that if term id is same in lang rows as is en row, then term is also the same."""

        lang_rows = Check.get_lang_rows(df, en_row)
        same_termid = lang_rows.loc[lang_rows[COLUMNS["term_id"]]
                                    == en_row[COLUMNS["term_id"]]]
        if not same_termid.empty:
            return same_termid[same_termid[COLUMNS["term"]] != en_row[COLUMNS["term"]]], "Term id same in en and lang rows but different term"
        return pd.DataFrame(), ""

    def __init__(self, password):
        self.__config = Config(password)
        self.__db = Database(self.__config)
        self.__excel = Excel(self.__config)

    def general_checks(self, df):
        """Run general checks on the entire dataframe."""

        invalid_values = {}
        df_checks = [
            Check.codeid_unique,
            Check.tmdc,
            Check.lang,
            Check.active,
            Check.legacy_concept_id,
            Check.legacy_term_id,
            Check.concept_fsn,
            Check.term,
            Check.beginning_date,
            Check.expiring_date,
            Check.concept_id_checksum,
            Check.term_id_checksum,
            Check.concept_id_legacy_concept_id,
            Check.term_id_legacy_term_id,
            Check.legacy_concept_id_legacy_term_id,
            Check.beginning_expiring_date,
            Check.expiring_date_active,
            Check.active_expiring_date,
            Check.no_overlap_concept_id,
            Check.no_overlap_term_id,
            Check.en_concept_id_is_linked_to_single_legacy_concept_id,
            Check.en_term_id_is_linked_to_single_legacy_term_id,
            Check.term_id_has_only_one_term
        ]
        for check in df_checks:
            sub_df, message = check(df)
            if not sub_df.empty:
                lineids = sub_df[COLUMNS["code_id"]].tolist()
                invalid_values[message] = lineids

        return invalid_values

    def en_row_checks(self, df):
        """Run checks on en rows + lang rows."""

        invalid_values = {}
        en_checks = [
            Check.concept_id_lang_same_as_concept_id_en,
            Check.concept_fsn_same_for_all_concept_id,
            Check.term_lang_same_as_term_en,
            Check.term_id_lang_same_as_term_id_en
        ]
        en_rows = df.loc[df[COLUMNS["lang"]] == "en"]
        for _, en_row in en_rows.iterrows():
            for check in en_checks:
                sub_df, message = check(df, en_row)
                if not sub_df.empty:
                    lineids = sub_df[COLUMNS["code_id"]].tolist()
                    if message in invalid_values:
                        invalid_values[message].extend(lineids)
                    else:
                        invalid_values[message] = lineids
        return invalid_values
    
    def write_invalid_values_to_dataframe(self, df, invalid_values: dict):
        """Write invalid values to a dataframe.

        The invalid values are in dict where key is the error message and value is a list of code ids.
        The dataframe should have code_id, error_message, and rest of the columns from the original dataframe.
        """
    
        # Initialize the dataframe with the required columns
        invalid_df = pd.DataFrame(columns=[COLUMNS["code_id"], "error_message"] + list(df.columns.drop(COLUMNS["code_id"])))

        for message, code_ids in invalid_values.items():
            for code_id in code_ids:
                # Get the row from the original dataframe and make a copy to avoid SettingWithCopyWarning
                row = df.loc[df[COLUMNS["code_id"]] == code_id].copy()
                # Add the error message to the row
                row["error_message"] = message
                # Reset the index of row to avoid InvalidIndexError during concatenation
                row.reset_index(drop=True, inplace=True)
                # Append the row to the invalid dataframe
                invalid_df = pd.concat([invalid_df, row], ignore_index=True)

        self.__excel.post_check(invalid_df)


    # def write_invalid_values_to_json(self, invalid_values):
    #     with open("invalid_values_2.json", "w") as f:
    #         json.dump(invalid_values, f, indent=4)

    def run(self, progress_callback=None):
        df = self.__db.get()
        if progress_callback:
            progress_callback(20)
        df = df[df[COLUMNS["active"]] == "Y"]
        if progress_callback:
            progress_callback(40)
        invalid_values = self.general_checks(df)
        if progress_callback:
            progress_callback(60)
        invalid_values.update(self.en_row_checks(df))
        if progress_callback:
            progress_callback(80)
        self.write_invalid_values_to_dataframe(df, invalid_values)
        if progress_callback:
            progress_callback(100)
