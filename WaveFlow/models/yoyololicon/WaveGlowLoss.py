import torch


# "Efficient" Loss Function
class WaveGlowLoss(torch.nn.Module):
    def __init__(self, hparams, elementwise_mean=True):
        super(WaveGlowLoss, self).__init__()
        sigma = hparams.sigma
        self.sigma2 = sigma ** 2
        self.sigma2_2 = self.sigma2 * 2
        self.mean = elementwise_mean
    
    def forward(self, model_outputs):
        z, logdet = model_outputs # [B, ...], logdet
        #loss = 0.5 * z.pow(2).sum(1) / self.sigma2 - logdet
        loss = z.pow(2).sum(1) / self.sigma2_2 - logdet
        loss = loss.mean()
        if self.mean:
            loss = loss / z.size(1)
        return loss