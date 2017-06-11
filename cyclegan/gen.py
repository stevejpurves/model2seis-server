# https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix

from torch.autograd import Variable
from torchvision import transforms
from PIL import Image

from options.train_options import TrainOptions

from models.models import create_model
import util.util as util

def load_cyclegan(opt):
    # Parse argument options
    
    opt.continue_train = True
    opt.name = 'test_model'
    opt.nThreads = 1 
    opt.batchSize = 1 
    opt.serial_batches = True
    opt.use_dropout = False
    opt.align_data = False
    opt.model = 'cycle_gan'
    opt.which_model_netG = 'resnet_9blocks'
    opt.continue_train = True
    opt.which_epoch = 3
    opt.which_direction = 'AtoB'
    opt.input_nc = 1
    opt.output_nc = 1
    opt.loadSize = 201
    opt.fineSize = 200
    opt.checkpoints_dir = './checkpoints'
    opt.ndf = 64
    opt.ngf = 64
    opt.nlayers = 3
    # Load model
    cyclegan = create_model(opt)
    return opt, cyclegan

def normalize_image(real, opt):
    # Load image
    preprocess = transforms.Compose([
        transforms.Scale(opt.loadSize),
        transforms.RandomCrop(opt.fineSize),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5),
                             (0.5, 0.5, 0.5)),
    ])  

    # Load input
    normed_real = preprocess(real).unsqueeze_(0)
    return normed_real

def model2seismic(normed_real, cyclegan):
    cyclegan.input_A.resize_(normed_real.size()).copy_(normed_real)
    cyclegan.test()
    seismic = util.tensor2im(cyclegan.fake_B.data)
    return seismic

def seismic2model(normed_real, cyclegan):
    cyclegan.input_B.resize_(normed_real.size()).copy_(normed_real)
    cyclegan.test()
    model = util.tensor2im(cyclegan.fake_A.data)
    return model

def main():
    opt = TrainOptions().parse()
    opt, cyclegan = load_cyclegan(opt)

    model = Image.open('./test_images/test_model.png').convert('L')
    seismic = Image.open('./test_images/test_seismic.png').convert('L')
	
    fake_model = seismic2model(normalize_image(seismic, opt), cyclegan)
    fake_seismic = model2seismic(normalize_image(model, opt), cyclegan)

    # Save image
    util.save_image(fake_model, './fake_model.png')
    util.save_image(fake_seismic, './fake_seismic.png')
    print(fake_model[0, 0:10])
    print(normalize_image(model, opt)[0, 0:10])

if __name__ == '__main__':
    main()
