import argparse
import collections

import numpy as np
import pandas as pd
from sklearn import metrics


def get_y_true():
    true_data_file = "data/sentihood/bert-sentclass-processed/processed_test_QA_M.tsv"

    df = pd.read_csv(true_data_file,sep='\t')
    y_true = []
    for i in range(len(df)):
        label = df['label'][i]
        assert label in ['None', 'Positive', 'Negative'], "error!"
        if label == 'None':
            n = 0
        elif label == 'Positive':
            n = 1
        else:
            n = 2
        y_true.append(n)
    
    return y_true


def get_y_pred(pred_data_dir):
    """ 
    Read file to obtain y_pred and scores.
    """
    pred=[]
    score=[]
    with open(pred_data_dir, "r", encoding="utf-8") as f:
        s=f.readline().strip().split()
        while s:
            pred.append(int(s[0]))
            score.append([float(s[1]),float(s[2]),float(s[3])])
            s = f.readline().strip().split()
    return pred, score


def sentihood_strict_acc(y_true, y_pred):
    """
    Calculate "strict Acc" of aspect detection task of Sentihood.
    """
    total_cases=int(len(y_true)/4)
    true_cases=0
    for i in range(total_cases):
        if y_true[i*4]!=y_pred[i*4]:continue
        if y_true[i*4+1]!=y_pred[i*4+1]:continue
        if y_true[i*4+2]!=y_pred[i*4+2]:continue
        if y_true[i*4+3]!=y_pred[i*4+3]:continue
        true_cases+=1
    aspect_strict_Acc = true_cases/total_cases

    return aspect_strict_Acc


def sentihood_macro_F1(y_true, y_pred):
    """
    Calculate "Macro-F1" of aspect detection task of Sentihood.
    """
    p_all=0
    r_all=0
    count=0
    for i in range(len(y_pred)//4):
        a=set()
        b=set()
        for j in range(4):
            if y_pred[i*4+j]!=0:
                a.add(j)
            if y_true[i*4+j]!=0:
                b.add(j)
        if len(b)==0:continue
        a_b=a.intersection(b)
        if len(a_b)>0:
            p=len(a_b)/len(a)
            r=len(a_b)/len(b)
        else:
            p=0
            r=0
        count+=1
        p_all+=p
        r_all+=r
    
    Ma_p=p_all/count
    Ma_r=r_all/count
    aspect_Macro_F1 = 2*Ma_p*Ma_r/(Ma_p+Ma_r)

    return aspect_Macro_F1


def sentihood_AUC_Acc(y_true, score):
    """
    Calculate "Macro-AUC" of both aspect detection and sentiment classification tasks of Sentihood.
    Calculate "Acc" of sentiment classification task of Sentihood.
    """
    # aspect-Macro-AUC
    aspect_y_true=[]
    aspect_y_score=[]
    aspect_y_trues=[[],[],[],[]]
    aspect_y_scores=[[],[],[],[]]
    for i in range(len(y_true)):
        if y_true[i]>0:
            aspect_y_true.append(0)
        else:
            aspect_y_true.append(1) # "None": 1
        tmp_score=score[i][0] # probability of "None"
        aspect_y_score.append(tmp_score)
        aspect_y_trues[i%4].append(aspect_y_true[-1])
        aspect_y_scores[i%4].append(aspect_y_score[-1])

    aspect_auc=[]
    for i in range(4):
        aspect_auc.append(metrics.roc_auc_score(aspect_y_trues[i], aspect_y_scores[i]))
    aspect_Macro_AUC = np.mean(aspect_auc)
    
    # sentiment-Macro-AUC
    sentiment_y_true=[]
    sentiment_y_pred=[]
    sentiment_y_score=[]
    sentiment_y_trues=[[],[],[],[]]
    sentiment_y_scores=[[],[],[],[]]
    for i in range(len(y_true)):
        if y_true[i]>0:
            sentiment_y_true.append(y_true[i]-1) # "Postive":0, "Negative":1
            tmp_score=score[i][2]/(score[i][1]+score[i][2])  # probability of "Negative"
            sentiment_y_score.append(tmp_score)
            if tmp_score>0.5:
                sentiment_y_pred.append(1) # "Negative": 1
            else:
                sentiment_y_pred.append(0)
            sentiment_y_trues[i%4].append(sentiment_y_true[-1])
            sentiment_y_scores[i%4].append(sentiment_y_score[-1])

    sentiment_auc=[]
    for i in range(4):
        sentiment_auc.append(metrics.roc_auc_score(sentiment_y_trues[i], sentiment_y_scores[i]))
    sentiment_Macro_AUC = np.mean(sentiment_auc)

    # sentiment Acc
    sentiment_y_true = np.array(sentiment_y_true)
    sentiment_y_pred = np.array(sentiment_y_pred)
    sentiment_Acc = metrics.accuracy_score(sentiment_y_true,sentiment_y_pred)

    return aspect_Macro_AUC, sentiment_Acc, sentiment_Macro_AUC


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred_data_dir",  default=None,  type=str, required=True, help="The pred data dir.")
    args = parser.parse_args()

    result = collections.OrderedDict()
    # task_name = "sentihood_QA_M"
    y_true = get_y_true()
    y_pred, score = get_y_pred(args.pred_data_dir)
    aspect_strict_Acc = sentihood_strict_acc(y_true, y_pred)
    aspect_Macro_F1 = sentihood_macro_F1(y_true, y_pred)
    aspect_Macro_AUC, sentiment_Acc, sentiment_Macro_AUC = sentihood_AUC_Acc(y_true, score)
    result = {'aspect_strict_Acc': aspect_strict_Acc,
            'aspect_Macro_F1': aspect_Macro_F1,
            'aspect_Macro_AUC': aspect_Macro_AUC,
            'sentiment_Acc': sentiment_Acc,
            'sentiment_Macro_AUC': sentiment_Macro_AUC}

    for key in result.keys():
        print(key, "=",str(result[key]))
    

if __name__ == "__main__":
    main()