# Paraphrase Model

To collect the paraphrase data, first download the [OpenStax Sentences dataset](http://www.kaggle.com/dataset/8c4350112049394cc697b89fec03846eee82942d3665c433cda01d6622553e19). Once this is completely, run "data_collection.ipynb". This will create two files "train_ds.json" and "test_ds.json".  

Once this is complete, you may train the model with the following code.

```
python paraphrase_generator.py
```
