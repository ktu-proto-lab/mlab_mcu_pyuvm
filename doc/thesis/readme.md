# Setup
## Linux
### Ubuntu/Debian
Install full [Tex Live](https://tug.org/texlive/) (~4GB):

```bash
sudo apt install texlive-full
```
This may take several minutes depending on your machine.

Also the template uses Microsoft fonts:

```bash
sudo apt install ttf-mscorefonts-installer
```

Follow the installation instructions.

#### Option 1

You can use [TeXstudio](https://www.texstudio.org/), a dedicated LaTeX editor:

```bash
sudo apt install texstudio
```

After installation, you can open it:

```bash
texstudio instructions.tex &
```
Go to:

`Options > Configure TeXstudio... > Build > Default Compiler > XeLaTeX > OK`

And:

`Options > Configure TeXstudio... > Build > Default Bibliography Tool > Biber > OK`

Press `F8` to run Biber to process `.bib` file.

Press `F5` to build and view.

#### Option 2

You may need to install [latexmk](https://miktex.org/packages/latexmk), but it should be already installed with texlive:

```bash
sudo apt install latexmk
```

You can use `latexmk` to build project:

```bash
# -pdfxe    : specifies to use xelatex
# -auxdir   : all build file (log, aux etc) directory
# -outdir   : final file (pdf) directory
latexmk -pdfxe -auxdir=build -outdir=. instructions.tex
```

And you can make a very simple makefile script using [GNU make](https://www.gnu.org/software/make/manual/make.html):

```makefile
all:
	latexmk -pdfxe -auxdir=build -outdir=. instructions.tex

clean:
	latexmk -c -auxdir=build -outdir=.
	rm -rf build
```

Usage:

```bash
# build (create pdf)
make
# clear all files
make clean
```

#### Option 3

Install your way.
