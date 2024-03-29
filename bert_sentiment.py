from transformers import BertForSequenceClassification
from torch import nn
import torch

class SentimentClassifier(nn.Module):

  def __init__(self, n_classes):

    super(SentimentClassifier, self).__init__()

    self.bert = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels = 3)
    self.bert.resize_token_embeddings(30524) #tokenizer vocab len:  30524 (added for LOCATION1 AND LOCATION2)

  def forward(self, input_ids, attention_mask, label_ids):

    outputs = self.bert(input_ids, attention_mask=attention_mask, labels=label_ids)
    return outputs