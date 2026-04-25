\LoadClass[12pt,a4paper]{article}
\RequirePackage[includefoot, left=3cm,right=1.8cm,top=1.8cm,bottom=1.8cm]{geometry}
\RequirePackage{graphicx}
\RequirePackage{xcolor}
\RequirePackage{scrextend}
\RequirePackage{fontspec}
\RequirePackage{sectsty}
\RequirePackage{titlesec}
\RequirePackage{secdot}
% Discourage hyphen usage
\RequirePackage[none]{hyphenat}
\RequirePackage{tocloft}
% add list of figures and list of tables to ToC
\RequirePackage[nottoc]{tocbibind}
\RequirePackage{caption}
\RequirePackage[lithuanian]{babel}
\RequirePackage{chngcntr}

\setmainfont{Times New Roman} % the document must use times new roman font

\definecolor{brown}{HTML}{D4AF37}
\definecolor{gray}{HTML}{808080}

\renewcommand\LARGE{\@setfontsize\LARGE{18}{18}}

\newcommand*\supervisor[1]{\gdef\@supervisor{#1}}
\newcommand*\@supervisor{\@latex@error{\noexpand\supervisor is not provided.}}
\newcommand*\authortext[1]{\gdef\@authortext{#1}}
\newcommand*\@authortext{Projekto autorius}
\newcommand*\supervisortext[1]{\gdef\@supervisortext{#1}}
\newcommand*\@supervisortext{Vadovas}
\newcommand*\reviewer[1]{\gdef\@reviewer{#1}}
\newcommand*\@reviewer{\@latex@error{\noexpand\reviewer is not provided.}}
\newcommand*\reviewertext[1]{\gdef\@reviewertext{#1}}
\newcommand*\@reviewertext{Recenzentas}
\newcommand*\authorgenitive[1]{\gdef\@authorgenitive{#1}}
\newcommand*\@authorgenitive{\@latex@error{\noexpand\authorgenitive is not provided.}}

% Lithuanian captions
\addto\captionslithuanian{%
  \renewcommand{\figurename}{pav.}%
  \renewcommand{\tablename}{lentelė.}
  \renewcommand{\contentsname}{Turinys}%
  \renewcommand{\listfigurename}{\texorpdfstring{\hfil}{\space}\fontsize{12}{15}{\selectfont{Paveikslų sąrašas}}}%
  \renewcommand{\listtablename}{\texorpdfstring{\hfil}{\space}\fontsize{12}{15}{\selectfont{Lentelių sąrašas}}}
}

% Try to avoid overfull.
\emergencystretch 3em%
\linespread{1.15}
\setlength{\parindent}{0cm}
% Fix spacing for sections by adding parfill option
\RequirePackage[parfill]{parskip}
\setlength{\parskip}{3.5mm}

% --- SECTIONS ---
\allsectionsfont{\fontsize{12}{15}\selectfont}
\sectiondot{subsection}
\sectiondot{subsubsection}
\newcommand{\centersection}[1]{
  \section*{\hfil#1}
  \addcontentsline{toc}{section}{#1}%
  }

\titlespacing{\section}{0pt}{3.5mm}{3.5mm}
\titlespacing{\subsection}{0pt}{2mm}{2mm}
\titlespacing{\subsubsection}{0pt}{2mm}{2mm}

% --- TABLES ---
% use tabularx for easy formatting of full page width tables
\RequirePackage{tabularx}
% allow table headers and set their style to footnotesize (10px) bold
\RequirePackage{makecell}
\renewcommand\theadfont{\footnotesize\bfseries}
% add spacing to table cell content, this should be 1.1 mm, but arraystretch accepts a coefficient rather than mm
\let\oldtabular\tabularx
\renewcommand{\tabularx}{\footnotesize\oldtabular}
\renewcommand{\arraystretch}{1.1}
% format table captions to effectively be "\textbf{1 lentelė.} Konkurentų apžvalga" in small size
\DeclareCaptionLabelFormat{ktucaptionlabel}{#2 #1}
\captionsetup[table]{labelformat=ktucaptionlabel,name=lentelė,labelsep=period,labelfont={bf,small},singlelinecheck=false,textfont=small,skip=1.1mm}
% List of tables configuration
\renewcommand{\cfttabaftersnum}{~lentelė.}
\renewcommand{\cfttabpresnum}{\bfseries}
% Looks like this value has to be fixed. Looks decent up to 99 tables.
% If anyone knows how to make this dynamic, make a PR
\setlength{\cfttabnumwidth}{5.3em}
% Remove indentation from LoT
\setlength{\cfttabindent}{0pt} 

% --- ToC ---
\renewcommand{\cfttoctitlefont}{\hfil\bfseries\selectfont}
\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}
% no vertical spacing between numberless sections
\setlength\cftparskip{0pt}
\setlength\cftbeforesecskip{0pt}
% dot frequency
\renewcommand\cftdotsep{2}
% no indentations for subsections and sections
\setlength{\cftsecindent}{0pt}
\setlength{\cftsubsecindent}{0pt}
\setlength{\cftsubsubsecindent}{0pt}
% add dots after ToC section numbers
\renewcommand{\cftsecaftersnum}{.}
\renewcommand{\cftsubsecaftersnum}{.}
\renewcommand{\cftsubsubsecaftersnum}{.}

% --- FIGURES ---
\renewcommand{\thefigure}{\arabic{figure}}

% Center figures
\g@addto@macro\@floatboxreset\centering

% List of figures configuration
\renewcommand{\cftfigaftersnum}{~pav.}
\renewcommand{\cftfigpresnum}{\bfseries}
% Looks like this value has to be fixed. Looks decent up to 99 images.
% If anyone knows how to make this dynamic, make a PR
\setlength{\cftfignumwidth}{4em}
% Remove indentation from LoF
\setlength{\cftfigindent}{0pt}
% setup figure captions
\captionsetup[figure]{labelsep=space, font=small, labelfont=bf, skip=0pt, justification=centering}


% --- BIBLIOGRAPHY ---
\RequirePackage[
  backend=biber,
  style=iso-numeric,
  maxbibnames=4,
]{biblatex}
\DeclareNameAlias{author}{sortname}
\RequirePackage{csquotes}
\DeclareQuoteAlias{czech}{lithuanian}

% --- PAGE NUMBERS ---
\RequirePackage{fancyhdr}
\fancyhead{}
\lfoot{} \cfoot{} \rfoot{\thepage}
\pagestyle{fancy}
% apply right-aligned page number to ToC, LoF, LoT
\fancypagestyle{plain}{\pagestyle{fancy}}
% remove fancyhdr headrule
\renewcommand{\headrulewidth}{0pt}
% don't indent footnotes
\RequirePackage[bottom,hang,flushmargin]{footmisc}

% Require enumitem for item list configuration
\RequirePackage{enumitem}
\setlist[itemize]{noitemsep, topsep=0pt}
\setlist[enumerate]{noitemsep, topsep=0pt}

% update style for enumerate - it should have no extra indent
\setlist[enumerate,1]{align=left}
% force each section to start on a new page
\newcommand{\sectionbreak}{\clearpage}

% --- Content ---

\renewcommand\maketitle{
  % First title page
  \thispagestyle{empty}  % hide page number
  {\parskip=0mm
    \begin{center}
      \vspace*{6.8mm}

      \includegraphics{logo}

      \vspace{10.6mm}
      \textbf{Kauno technologijos universitetas}

      \vspace{2.1mm}
      Informatikos fakultetas
      \vspace{33.5mm}

      {\LARGE \textbf{\@title}}

      \vspace{2.1mm}
      {\large Baigiamasis bakalauro studijų projektas}
      \vspace{33.1mm}

      \noindent{\textcolor{brown}{\rule{9cm}{0.5pt}}}
      \vspace{9mm}

      \parbox[s]{9cm}{\centering \textbf{\@author}}
      \vspace{2.1mm}

      \@authortext
      \vspace{6.5mm}

      \parbox[s]{9cm}{\centering \textbf{\@supervisor}}
      \vspace{2.1mm}

      \@supervisortext
      \vspace{6.5mm}

      \noindent{\textcolor{brown}{\rule{9cm}{0.5pt}}}

      \vfill

      \textbf{Kaunas, \the\year}
      \vspace{7mm}
    \end{center}
  }
  \clearpage
  % second page
  \thispagestyle{empty}
  {\parskip=0mm
    \begin{center}
      \vspace*{6.8mm}

      \includegraphics{logo}

      \vspace{10.6mm}
      \textbf{Kauno technologijos universitetas}
      \vspace{2.1mm}

      Informatikos fakultetas
      \vspace{33mm}

      {\LARGE \textbf{\@title}}
      \vspace{2.1mm}

      {\large Baigiamasis bakalauro studijų projektas}
      \vspace{2.1mm}

      {\large Programų sistemos (612I30002)}
      \vspace{18mm}

    \end{center}
    \begin{addmargin}[8cm]{0cm}
      \noindent{\textcolor{brown}{\rule{9cm}{0.5pt}}}
      \vspace{6mm}

      \noindent{\parbox[s]{7cm}{\textbf{\@author}}}
      \vspace{2.1mm}

      \noindent{\@authortext}
      \vspace{8.6mm}

      \noindent{\parbox[s]{7cm}{\textbf{\@supervisor}}}
      \vspace{2.1mm}

      \noindent{\@supervisortext}
      \vspace{8.6mm}

      \noindent{\parbox[s]{7cm}{\textbf{\@reviewer}}}
      \vspace{2.1mm}

      \noindent{\@reviewertext}
      \vspace{6mm}

      \noindent{\textcolor{brown}{\rule{9cm}{0.5pt}}}

    \end{addmargin}
    \begin{center}
      \vfill
      \textbf{Kaunas, \the\year}
      \vspace{7mm}
    \end{center}
  }
  \clearpage
  \thispagestyle{empty}
  {\parskip=2.1mm
    \begin{center}
      \vspace*{6.8mm}

      \includegraphics{logo}

      \vspace{8.4mm}
      \textbf{Kauno technologijos universitetas}

      Informatikos fakultetas

      \@author
      \vspace{24.6mm}

      {\LARGE \textbf{\@title}}

      {\large{Akademinio sąžiningumo deklaracija}}
      \vspace{11.9mm}
    \end{center}
  }

  Patvirtinu, kad mano, \@authorgenitive, baigiamasis projektas tema „\@title“ yra parašytas visiškai savarankiškai ir
  visi pateikti duomenys ar tyrimų rezultatai yra teisingi ir gauti sąžiningai.
  Šiame darbe nei viena dalis nėra plagijuota nuo jokių spausdintinių ar internetinių šaltinių, visos kitų šaltinių
  tiesioginės ir netiesioginės citatos nurodytos literatūros nuorodose.
  Įstatymų nenumatytų piniginių sumų už šį darbą niekam nesu mokėjęs.

  Aš suprantu, kad išaiškėjus nesąžiningumo faktui, man bus taikomos nuobaudos, remiantis Kauno technologijos
  universitete galiojančia tvarka.

  \vspace{7mm}

  \begin{addmargin}[56.6mm]{0cm}
    \begin{tabular}{p{70.7mm}@{\hskip 7.1mm}p{35.7mm}}
      \hrulefill & \hrulefill \\
      \multicolumn{1}{c}{\textcolor{gray}{{\normalsize (vardą ir pavardę įrašyti ranka)}}} &
      \multicolumn{1}{c}{\textcolor{gray}{{\normalsize (parašas)}}}
    \end{tabular}
  \end{addmargin}
  \clearpage
}
