## Random Forest Grid Search for number of trees and warm start.
## Evaluation of parameter optimization. 

import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from tempfile import mkdtemp
from sklearn import preprocessing
from sklearn import pipeline
from tempfile import mkdtemp
import warnings

warnings.filterwarnings("ignore")
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_curve, auc
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import roc_curve, auc
from sklearn.multiclass import OneVsRestClassifier
from matplotlib import pyplot as plt
import itertools


def grid_scores_to_df(grid_scores):
    """
    Convert a sklearn.grid_search.GridSearchCV.grid_scores_ attribute to a tidy
    pandas DataFrame where each row is a hyperparameter-fold combinatination.
    """
    rows = list()
    for grid_score in grid_scores:
        for fold, score in enumerate(grid_score.cv_validation_scores):
            row = grid_score.parameters.copy()
            row['fold'] = fold
            row['score'] = score
            rows.append(row)
    df = pd.DataFrame(rows)
    return df


def add_cv_mean(df, cv, col_name):
    for i in range(0, len(df), cv):
        df.loc[i, col_name] = np.mean(df.loc[i:(i + cv), 'score'])


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    X_train_val = pd.read_csv('../Data/dataFiles/Training_X_w_est_id.csv')
    y_train_val = pd.read_csv('../Data/dataFiles/Training_y_w_est_id.csv')
    X_test = pd.read_csv('../Data/dataFiles/Testing_X_w_est_id.csv')
    y_test = pd.read_csv('../Data/dataFiles/Testing_y_w_est_id.csv')
    cachedir = mkdtemp()

    estimators = [('normalize', preprocessing.StandardScaler()),
                  ('model', RandomForestClassifier())]
    pipe = pipeline.Pipeline(estimators, cachedir)

    num_trees = [50 + 50 * i for i in range(0, 2)]

    ws = [True, False]
    params = {'model__n_estimators': num_trees, 'model__warm_start': ws}
    grid = GridSearchCV(pipe, param_grid=params, cv=5)
    fittedgrid = grid.fit(X_train_val, y_train_val)
    grid_scores = fittedgrid.grid_scores_

    df_means = grid_scores_to_df(fittedgrid.grid_scores_)

    add_cv_mean(df_means, 5, 'mean')
    df_new = df_means.dropna()
    sns.set(style="ticks")

    means_true = df_new[df_new['model__warm_start'] == True]['mean']
    means_false = df_new[df_new['model__warm_start'] == False]['mean']
    x = np.unique(df_new['model__n_estimators'])
    fig = plt.figure()
    plt.plot(x, means_true, label='ws:True')
    plt.plot(x, means_false, label='ws:False')
    plt.xlabel('Number of Trees', size=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.ylabel('Cross-Val Score', size=14)
    plt.legend(loc='lower right', fontsize=14)
    plt.title('Parameter Optimization', size=18)
    my_dpi = 96
    plt.savefig('RF_parameter_opt_MultiClass_V2.png', dpi=my_dpi * 2, bbox_inches='tight')

    RF_predicts = fittedgrid.predict(X_test.drop(['establishment_id'], axis=1))
    RF_probs = fittedgrid.predict_proba(X_test.drop(['establishment_id'], axis=1))

    RF_best_score = fittedgrid.score(X_test.drop(['establishment_id'], axis=1), y_test)
    print(RF_best_score)

    confusion = confusion_matrix(y_test, RF_predicts)
    class_names = ['Crucial', 'Minor', 'None/Pass', 'Significant']

    plot_confusion_matrix(confusion, classes=class_names,
                          title='Confusion matrix, without normalization')
    plt.savefig('RF_Conf_multiclass_mat.png', dpi=my_dpi * 2, bbox_inches='tight')

    X_train = pd.read_csv('../Data/dataFiles/Training_X_w_est_id.csv')
    X_train = X_train.drop(['establishment_id'], axis=1)
    X_test = X_test.drop(['establishment_id'], axis=1)
    y_train = pd.read_csv('../Data/dataFiles/Training_y_w_est_id.csv', header=None)
    classifier = OneVsRestClassifier(fittedgrid.best_estimator_)

    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    titles = ['Crucial', 'Minor', 'None', 'Significant']
    f1 = []
    presc = []
    rec = []
    preds = classifier.fit(X_train, y_train).predict(X_test)
    probs = classifier.fit(X_train, y_train).predict_proba(X_test)

    # Plot ROC Curve
    for i in range(0, len(classifier.classes_)):
        y_test_1 = np.where(y_test == classifier.classes_[i], 1, 0)
        fpr, tpr, _ = roc_curve(y_test_1, probs[:, i])
        roc_auc = auc(fpr, tpr)
        preds_1 = np.where(preds == classifier.classes_[i], 1, 0)

        f1.append((100 * f1_score(preds_1, y_test_1)))
        presc.append(precision_score(preds_1, y_test_1))
        rec.append(recall_score(preds_1, y_test_1))

        plt.figure()
        lw = 2
        plt.plot(fpr, tpr,
                 lw=lw)
        plt.plot([0, 1], [0, 1], lw=lw, linestyle='--')
        plt.xlabel('False Positive Rate', size=14)
        plt.ylabel('True Positive Rate', size=14)
        plt.title(titles[i], size=16)

        plt.text(0.05, 0.95, 'AUC = %0.2f' % roc_auc, color='firebrick')
        plt.text(0.05, 0.85, 'F1 = %0.2f' % f1[i], color='firebrick')
        plt.text(0.05, 0.75, 'Precision = %0.2f' % presc[i], color='firebrick')
        plt.text(0.05, 0.65, 'Recall = %0.2f' % rec[i], color='firebrick')

        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        filename = titles[i] + 'roc_curve_RandomForest_v2.png'
        plt.savefig(filename, dpi=my_dpi * 2, bbox_inches='tight')

        plt.show()
