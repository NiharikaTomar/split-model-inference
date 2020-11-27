import torch

from model.split_model import *


def save_model(model, filepath):
    torch.save(model.state_dict(), filepath)
    print('Model is saved!')


def load_model(filepath, hparams):
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    model = SpeechRecognitionModel(
        hparams['n_cnn_layers'], hparams['n_rnn_layers'], hparams['rnn_dim'],
        hparams['n_class'], hparams['n_feats'], hparams['stride'], hparams['dropout']
    ).to(device)

    model.load_state_dict(torch.load(filepath))
    model.eval()

    return model


def load_split_model(filepath, hparams):
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    model_head = SpeechRecognitionModel_Head(
        hparams['n_cnn_layers'], hparams['n_rnn_layers'], hparams['rnn_dim'],
        hparams['n_class'], hparams['n_feats'], hparams['stride'], hparams['dropout']
    ).to(device)
    model_tail = SpeechRecognitionModel_Tail(
        hparams['n_cnn_layers'], hparams['n_rnn_layers'], hparams['rnn_dim'],
        hparams['n_class'], hparams['n_feats'], hparams['stride'], hparams['dropout']
    ).to(device)

    model_head.load_state_dict(torch.load(filepath))
    model_tail.load_state_dict(torch.load(filepath))
    model_head.eval()
    model_tail.eval()

    return model_head, model_tail