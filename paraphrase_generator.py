import os
from transformers import T5TokenizerFast, T5ForConditionalGeneration
import pytorch_lightning as pl
import torch
import json
from torch.utils.data import TensorDataset, random_split
from transformers.optimization import AdamW
from pytorch_lightning.callbacks import Callback
from tqdm import tqdm


device = 'cuda' if torch.cuda.is_available() else 'cpu'
save_path = './Models/paraphrase_8'

try:
    os.mkdir(save_path)
except:
    pass


class ParaphraseGenerator(pl.LightningModule):
    def __init__(self):
        super().__init__()
        model_name = 't5-base'
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = T5TokenizerFast.from_pretrained(model_name)
        self.batch_size = 12
        self.lr = 4e-5

    def encode_text(self, data_path):
        with open(data_path, 'r', encoding='utf-8') as r:
            data = json.load(r)
        for item in tqdm(data):
            # tokenizing original and paraphrase:
            source = self.tokenizer(
                item['Source'], max_length=80, truncation=True, padding='max_length', return_tensors='pt')
            target = self.tokenizer(
                item['Target'], max_length=200, truncation=True, padding='max_length', return_tensors='pt')
            yield source['input_ids'], target['input_ids']

    def to_tensor(self, source_ids, target_ids):
        source_ids = torch.cat(source_ids, dim=0)
        target_ids = torch.cat(target_ids, dim=0)
        data = TensorDataset(source_ids, target_ids)
        return random_split(data, [len(data), 0])[0]

    def prepare_data(self):
        source_ids, target_ids = list(
            zip(*tuple(self.encode_text('train_ds.json'))))
        self.train_ds = self.to_tensor(source_ids, target_ids)

        source_ids, target_ids = list(
            zip(*tuple(self.encode_text('test_ds.json'))))
        self.test_ds = self.to_tensor(source_ids, target_ids)

    def forward(self, batch, batch_idx):
        source_ids, target_ids = batch[:2]
        return self.model(input_ids=source_ids, labels=target_ids)

    def training_step(self, batch, batch_idx):
        loss = self(batch, batch_idx)[0]
        self.log('train_loss', loss)
        return loss


    def validation_step(self, batch, batch_idx):
        loss = self(batch, batch_idx)[0]
        self.log('val_loss', loss)

    def train_dataloader(self):
        return torch.utils.data.DataLoader(self.train_ds, batch_size=self.batch_size, drop_last=True, shuffle=True, num_workers=0)

    def val_dataloader(self):
        return torch.utils.data.DataLoader(self.test_ds, batch_size=self.batch_size, drop_last=False, shuffle=False, num_workers=0)

    def configure_optimizers(self):
        return AdamW(self.parameters(), lr=self.lr, weight_decay=0.01)


class SaveCallback(Callback):
    def on_epoch_start(self, trainer, pl_module):
        if pl_module.current_epoch > 0:
            current_epoch = str(pl_module.current_epoch)
            fn = f'epoch_{current_epoch}'
            new_path = f"{save_path}/{fn}/"
            if fn not in os.listdir(save_path):
                os.mkdir(new_path)
            pl_module.tokenizer.save_vocabulary(new_path)
            pl_module.model.save_pretrained(new_path)


trainer = pl.Trainer(
    default_root_dir='logs',
    min_epochs=4,
    gpus=-1,
    max_epochs=5,
    val_check_interval=0.5,
    callbacks=[SaveCallback()],
    logger=pl.loggers.TensorBoardLogger('logs/', name='paraphrase', version=0)
)


para_model = ParaphraseGenerator()
trainer.fit(para_model)
