import sys
import keras

import csv

csv.field_size_limit(sys.maxsize)


from texcla import experiment

from texcla.preprocessing import FastTextWikiTokenizer
from texcla.data import Dataset
from texcla.models import YoonKimCNN, TokenModelFactory

data_path = 'out.csv'
proc_path = './proc.bin'
max_len = 200


def train_cnn(lr=0.001, batch_size=1024, dropout_rate=0.5, filter_sizes=[3, 4, 5], num_filters=20, results_base_dir=None):
    word_encoder_model = YoonKimCNN(
        filter_sizes=filter_sizes, num_filters=num_filters, dropout_rate=dropout_rate)
    train(word_encoder_model, lr, batch_size, results_base_dir)


def train(word_encoder_model, lr, batch_size, results_base_dir):
    ds = Dataset.load(proc_path)

    factory = TokenModelFactory(
        ds.num_classes, ds.tokenizer.token_index, max_tokens=max_len, embedding_type="fasttext.wiki.de", embedding_dims=300)

    model = factory.build_model(
        token_encoder_model=word_encoder_model, trainable_embeddings=False)

    experiment.train(x=ds.X, y=ds.y, validation_split=0.1, model=model, word_encoder_model=word_encoder_model, epochs=5)


def build_dataset():
    tokenizer = FastTextWikiTokenizer()

    X_con, y = experiment.load_csv(data_path, text_col='content', class_col='is_foi')
    X_sub, _ = experiment.load_csv(data_path, text_col='subject', class_col='is_foi')

    # join subject and content
    X = ['. '.join(li) for li in zip(X_con, X_sub)]

    experiment.setup_data(X, y, tokenizer, proc_path, max_len=max_len)


def train_stacked():
    pass


def main():
    if len(sys.argv) != 2:
        raise ValueError('You have to specify a positional command!')
    if sys.argv[1] == 'setup':
        build_dataset()
    if sys.argv[1] == 'traincnn':
        train_cnn()
    if sys.argv[1] == 'trainstacked':
        train_stacked()


if __name__ == '__main__':
  main()