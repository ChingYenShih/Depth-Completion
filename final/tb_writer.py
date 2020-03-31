from dataloader.dataloader import get_loader
from training.utils import normal_to_0_1
from tensorboardX import SummaryWriter

class TensorboardWriter():
    def __init__(self, path):
        self.writer = SummaryWriter(path)

    def get_testing_img(self):
        """Load one example for visualizing result in each epoch.
           Use tensorboard to visualize this example

        Returns:
        rgb: rgb input of the model (1 x c x w x h)
        lidar: lidar input of the model
        mask: mask input of the model
        """
        loader = get_loader('val', shuffle=False, num_data=1, crop=False)
        for rgb, lidar, mask, gt_depth, params, gt_surface_normal, gt_normal_mask in loader:
            self.writer.add_image('RGB input', rgb[0] / 255.0, 1)
            self.writer.add_image('lidar input', lidar[0], 1)
            self.writer.add_image('GroundTruth depth', normal_to_0_1(gt_depth[0]), 1)
            self.writer.add_image('GroundTruth surface normal', normal_to_0_1(gt_surface_normal[0]), 1)
            return rgb, lidar, mask

    def tensorboard_write(self, epoch, train_losses, val_losses, predicted_dense, pred_surface_normal):
        """Write every epoch result on the tensorboard

        Params:
        epoch: int
        train_losses: list of different type of training loss, [loss, loss_d, loss_c, loss_n, loss_normal]
        val_losses: list of different type of val loss, [loss, loss_d, loss_c, loss_n, loss_normal]
        predicted_dense: predicted dense depth from model (1 x c x h x w)
        pred_surface_normal: predicted surface normal from model (1 x c x h x w)
        """
        
        loss_type = ['loss', 'loss_d', 'loss_c', 'loss_n', 'loss_normal']

        for i, t in enumerate(loss_type):
            self.writer.add_scalar('train_{}'.format(t), train_losses[i], epoch)
            self.writer.add_scalar('val_{}'.format(t), val_losses[i], epoch)
        self.writer.add_image('predicted_dense', normal_to_0_1(predicted_dense[0]), epoch)
        self.writer.add_image('pred_surface_normal', normal_to_0_1(pred_surface_normal[0]), epoch)

    def close(self):
        self.writer.close()
