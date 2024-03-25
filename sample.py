from torchvision.utils import save_image
from diffusion_model import DiffusionModel
from utils import generate_animation, get_custom_context
import os
import argparse

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Sample images from diffusion model")
    parser.add_argument("--checkpoint-name", type=str, default="checkpoint_0.pth", help="Checkpoint name of diffusion model")
    parser.add_argument("--n-samples", type=int, default=100, help="Number of samples to generate")
    parser.add_argument("--n-images-per-row", type=int, default=10, help="Number of images each row contains in the grid")
    parser.add_argument("--device", type=str, default="cuda", help="GPU device to use")
    parser.add_argument("--timesteps", type=int, default=None, help="Total timesteps for sampling")
    parser.add_argument("--beta1", type=float, default=None, help="Hyperparameter for dppm")
    parser.add_argument("--beta2", type=float, default=None, help="Hyperparameter for ddpm")
    
    args = parser.parse_args()
    
    os.makedirs(os.path.join(os.path.dirname(__file__), "generated-images"), exist_ok=True)
    
    diffusion_model = DiffusionModel(device=args.device, checkpoint_name=args.checkpoint_name)
    c = get_custom_context(n_samples=args.n_samples, n_classes=diffusion_model.nn_model.n_cfeat, device=diffusion_model.device)
    samples, intermediate_ddpm, t_steps = diffusion_model.sample_ddpm(args.n_samples, c, 20, args.timesteps, args.beta1, args.beta2)
    
    save_image(samples, os.path.join(os.path.dirname(__file__), "generated-images", 
                                    f"{diffusion_model.dataset_name}_ddpm_images.jpeg"), 
                                    scale_each=True, normalize=True, nrow=args.n_images_per_row)
    generate_animation(intermediate_ddpm, t_steps, os.path.join(os.path.dirname(__file__), "generated-images",
                                                       f"{diffusion_model.dataset_name}_ani.gif"), 
                                                       n_images_per_row=args.n_images_per_row)
