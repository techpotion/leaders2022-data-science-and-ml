import pandas as pd
import numpy as np
from tqdm import tqdm

id_features = [
    "root_id",
    "version_id",
    "request_number",
    "mos_ru_request_number",
    "root_identificator_of_maternal",
    "number_of_maternal",
    "deffect_category_id",
    "deffect_id",
    "district_code",
    "hood_code",
    "performing_company",
    "inn_of_performing_company",
    "id_of_reason_for_decline", # all values are NaN in taken sample
    "id_of_reason_for_decline_of_org",   # all values are NaN in taken sample
    "id_work_type_done",
    "id_guarding_events"
]

date_features = [
    "date_of_creation",
    "date_of_start",
    "wanted_time_from",
    "wanted_time_to",
    "date_of_review",
    "date_of_last_return_for_revision",
    "closure_date"
]

# All numerical features are discrete -> casting to Int64
numerical_features = [
    "times_returned",    # might be useful
    "adress_unom"
]

categorical_features = [
    "name_of_source",
    "name_of_source_eng",
    "name_of_creator",
    "role_of_user",
    "deffect_category_name",
    "deffect_category_name_eng",
    "deffect_name",
    "short_deffect_name",
    "need_for_revision",
    "urgency_category",
    "urgency_category_eng",
    "district",
    "hood",
    "adress_of_problem",
    "incident_feature",
    "serving_company",
    "dispetchers_number",
    "request_status",
    "request_status_eng",
    "reason_for_decline",   # all values are NaN in taken sample
    "reason_for_decline_of_org", # all values are NaN in taken sample
    "efficiency",
    "efficiency_eng",
    "being_on_revision",
    "alerted_feature",
    "grade_for_service",
    "grade_for_service_eng",
    "payment_category",
    "payment_category_eng",
    "payed_by_card"
]

# String features can also be categorical with a lot of possible values
string_features = [
    "last_name_redacted",
    "commentaries", # might be useful
    "code_of_deffect",
    "description",  # might be useful
    "presence_of_question", # might be useful

    "dispetchers_number",
    "owner_company",
    "work_type_done", # might be useful
    "used_material",
    "guarding_events", # might be useful
    "review",    # might be useful - here is the information about the results of the work

    # These are numerical features, that include some strangely filled rows:
    "floor",
    "flat_number",
    "porch",
]

features = string_features + date_features + numerical_features + categorical_features + id_features

def change_columns(df, naming_path) -> pd.DataFrame:
    '''
    Function which changes column names for pd.DataFrame
    '''
    
    new_names = list(
        map(
            lambda x: x.strip(),
            list(pd.read_csv(naming_path)['new_name'])
        )
    )
    df.columns = new_names

    return df

# Изменение типов колонок:
def cast_types(df) -> pd.DataFrame:

    to_str = string_features + categorical_features + id_features

    for feature in to_str:
        df = df.astype({
            feature: "str"
        })

    for feature in numerical_features:
        df = df.astype({
            feature: "Int64"
        })

    for feature in date_features:
        df = df.astype({
            feature: "datetime64[ns]"   # if the time precission is given up to ns - that's the format
        })
    
    return df

def transform_df(df, naming_path):
    df = cast_types(change_columns(df, naming_path))

    return df

def df_iter_into_df(df_iter, naming_path):
    for i, df in tqdm(enumerate(df_iter)):
        df = transform_df(df, naming_path=naming_path)
        if i == 0:
            result_df = df
        result_df = pd.concat([df, result_df])
    return result_df

def tils_parse_date(self, string):
    try:
        return np.datetime64(string) 
    except:
        return