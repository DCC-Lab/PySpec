from .spectrumuncurver import *
import argparse


parser = argparse.ArgumentParser(description="Tool to uncurve and graph spectrometer data.", prog="python -m spectrumuncurver")

parser.add_argument('imagePath', type=str,
                    help='The image that will be processed.')

parser.add_argument('xyPeakLimits', type=int, nargs=4,
                    help='xmin, xmax, ymin, ymax position for peak curve analysis.')

parser.add_argument('method', type=str,
                    help="chose between 'maximum', 'gaussian'")

group = parser.add_mutually_exclusive_group()

group.add_argument('-U', '--uncurve', action='store_true',
                    help='Will prompt you to save the uncurved file.')

group.add_argument('-S', '--superpose', action='store_true',
                    help='Will prompt you to save the curved image superposed with the peak data.')

group.add_argument('-P', '--plot', action='store_true',
                   help='Will prompt you to save the uncurved and summed specturm plot.')

args = parser.parse_args()

print(args.imagePath)
print(args.xyPeakLimits)
try:

    spectrumUncurver = SpectrumUncurver()
    spectrumUncurver.load_image(args.imagePath)
    spectrumUncurver.uncurve_spectrum_image([args.xyPeakLimits[0], args.xyPeakLimits[1]], [args.xyPeakLimits[2], args.xyPeakLimits[3]], args.method)

    if args.uncurve:
        spectrumUncurver.save_uncurved_image()
    elif args.superpose:
        spectrumUncurver.save_image_with_fit()
    elif args.plot:
        print("ask to save the plot")

except Exception as e:
    print(e)
