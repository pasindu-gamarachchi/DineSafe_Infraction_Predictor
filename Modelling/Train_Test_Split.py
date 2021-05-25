import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
import os
import warnings

warnings.filterwarnings("ignore")


def check_and_drop_cols(df, cols):
    for i in cols:
        if i in df.columns:
            df = df.drop(i, axis=1)
    return df


if __name__ == '__main__':
    df = pd.read_csv('..\Data\dataFiles\Cleaned_Data.csv', index_col=0)
    cols_2_drop = ['Unnamed: 0', 'severity', 'inspection_date']
    df = check_and_drop_cols(df, cols_2_drop)

    y = df['label_severity']
    X = df.drop(['label_severity'], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.73, random_state=12)
    X_train.to_csv('Training_X_w_est_id.csv', index=False)
    X_test.to_csv('Testing_X_w_est_id.csv', index=False)
    y_train.to_csv('Training_y_w_est_id.csv', index=False)
    y_test.to_csv('Testing_y_w_est_id.csv', index=False)
