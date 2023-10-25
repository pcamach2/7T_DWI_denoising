# Usage: profiler.py <subject> <denoising_method> <n_jobs> <output_dir>
import argparse
import pyinstrument
import subprocess
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Denoising speed test')
parser.add_argument('subject', type=str, help='Subject to denoise')
parser.add_argument('denoising_method', type=str,
                    help='Denoising method to use')
parser.add_argument('n_jobs', type=int, help='Number of jobs for parallel processing')
parser.add_argument('output_dir', type=str, help='Output directory')

args = parser.parse_args()

# Define the command to run the denoising_speed_test.py script
command = f"python /scripts/denoising_speed_test_simple.py {args.output_dir} {args.subject} {args.denoising_method} {args.n_jobs}"

# Use Pyinstrument to profile the script
profiler = pyinstrument.Profiler()
profiler.start()
subprocess.run(command, shell=True)
profiler.stop()

# Save the results to a file in the /timer directory
results_file = "/timer/" + args.subject + "_" + \
    args.denoising_method + "_" + str(args.n_jobs) + "_denoising_speed_test_results.txt"
with open(results_file, "w") as f:
    f.write(profiler.output_text(unicode=True, color=True))

# # plot the results of profiling
# plt.figure()
# profiler.output_html()
# plt.savefig("/timer/" + args.subject + "_" + \
#     args.denoising_method + "_" + str(args.n_jobs) + "_denoising_speed_test_results.png")

