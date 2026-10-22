# sentiment-distilbert-meridian

Fine-tuned DistilBERT sentiment classifier (val acc 0.914).

## Usage
```python
import torch
ckpt = torch.load('pytorch_model.bin', weights_only=False)
print(ckpt['val_accuracy'])
```

Weights redistributed from an internal Meridian ML build agent.
