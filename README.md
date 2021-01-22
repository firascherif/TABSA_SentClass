# TABSA SentClass

## Requirement

* pytorch: 1.0.0
* python: 3.7.1
* tensorflow: 1.13.1
* numpy: 1.15.4
* nltk
* sklearn

## Étape 1: préparer les ensembles de données

Le jeu de données: `data/sentihood/`.

Exécutez les commandes suivantes pour préparer les ensembles de données pour les tâches:

```
cd generate/
python3 generate_sentihood_SentClass.py
```

## Étape 2: train

Par exemple, **bert-sentclass** sur le jeu de données **SentiHood**:

```
python3 bert_sentclass.py \
--num_train_epochs 8 \
--max_seq_length 512 \
--batch_size 8 \
--learning_rate 1e-5 \
--output_dir results/new_folder/
```

Nous avons ajouté l’option pour sauvegarder le modèle entrainé dans le dossier « Results ». 
Nous pouvons donc passer --init_checkpoint comme argument.


## Étape 3: evaluation

Évaluez les résultats sur l'ensemble de test (calculez Precision, F-mesure, etc.).
L'exemple suivant affiche les resultats de l'epoch 7.

```
python3 evaluation_sentclass.py --pred_data_dir results/bert_test_ep_7.txt
```

# SVM
* Le modele SVM se trouve ici: `modele_de_base_svm/execution_svm.ipynb`. 
* Pour entrainer et tester le modèle, il suffit de lancer le notebook.
