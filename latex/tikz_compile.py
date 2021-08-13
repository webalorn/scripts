from pathlib import Path
import sys, os, subprocess
import random, string
import platform

# ----------------------------------------
# Compile TIKZ and drawio files into pdf
# ----------------------------------------

tmp_filename = "tmp_comp_" + "".join(random.choices(string.ascii_lowercase, k=12))
tmp_dir = tmp_filename + "_build"
filename_latex = tmp_filename + ".tex"
script_dir = Path(__file__).parent.resolve()
figure_path = None

OS_NAME = platform.system() # In ['Linux', 'Darwin', 'Windows']

def get_modif_time(p):
	try:
		return os.path.getmtime(str(p))
	except FileNotFoundError:
		return 0

def compile_file(tikzfile):
	tikz_pdf = tikzfile.with_suffix("").with_suffix(".pdf")
	if get_modif_time(tikz_pdf) >= get_modif_time(tikzfile):
		return False

	compile_dir = tikzfile.parent.resolve()
	os.chdir(str(compile_dir))
	os.system("mkdir -p " + tmp_dir)
	try:
		with open(str(script_dir / "template_tikz.tex"), "r") as f:
			template_code = f.read()
		with open(str(tikzfile), "r") as f:
			latex_code = template_code.replace("<latex_code>", f.read())
		latex_code = latex_code.replace("<figures_path>", figure_path)

		with open(filename_latex, "w") as tmp_latex_file:
			tmp_latex_file.write(latex_code)

		r = subprocess.run(
			("xelatex -interaction=nonstopmode -output-directory="+tmp_dir+" "+filename_latex).split(),
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)
		if r.returncode:
			print("======== Error during the compilation")
			print(r.stdout.decode('utf-8'), "\n\n", r.stderr.decode('utf-8'))
			raise Exception("Error during the compilation")
		tmp_pdf = tikzfile.parent / tmp_dir / (tmp_filename + ".pdf")
		tmp_pdf.rename(tikz_pdf)
	finally:
		os.system("rm " + filename_latex)
		os.system("rm -R " + tmp_dir)
	return True

def convert_drawio(drawio_file):
	pdf_file = drawio_file.with_suffix(".pdf")
	if get_modif_time(pdf_file) >= get_modif_time(drawio_file):
		return False

	drawio_command = "drawio"
	if OS_NAME == 'Darwin':
		drawio_command = "/Applications/draw.io.app/Contents/MacOS/draw.io"
	r = subprocess.run(
		(f"{OS_NAME}  --crop -x -o {str(pdf_file.resolve())} {str(drawio_file.resolve())}").split(),
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE
	)
	if r.returncode:
		print("======== Error during the compilation")
		print(r.stdout.decode('utf-8'), "\n\n", r.stderr.decode('utf-8'))
		raise Exception("Error during the compilation")

	return True

def compile_if_tikz(tikzfile):
	if tikzfile.name.endswith(".tz.tex"):
		print("Compiling {} ...".format(tikzfile.name))
		if not compile_file(tikzfile):
			print("-> Already up to date")
		else:
			print("=> Done")

def compile_if_drawio(drawio_file):
	if drawio_file.name.endswith(".drawio"):
		print("Compiling {} ...".format(drawio_file.name))
		if not convert_drawio(drawio_file):
			print("-> Already up to date")
		else:
			print("=> Done")

def recursive_tikz(p):
	for subfile in p.iterdir():
		if subfile.is_file():
			compile_if_tikz(subfile)
			compile_if_drawio(subfile)
		elif subfile.is_dir():
			recursive_tikz(subfile)

def main():
	global figure_path
	"""
		Compile all files tz_<name>.tex in the current directory or the given directory. It must be the root of the project, with the "figures" directory.
	"""
	p = Path(".")
	if len(sys.argv) >= 2:
		p = Path(sys.argv[1])
	# figure_path = str((p/"figures").resolve())
	recursive_tikz(p)

if __name__ == '__main__':
	main()