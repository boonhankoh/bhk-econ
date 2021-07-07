By Chance or by Choice? Biased Attribution of Others' Outcomes when Social Preferences Matter
by Nisvan Erkal, Lata Gangadharan, and Boon Han Koh

1) The "Experimental Program" folder contains the required z-Tree (Exp 1) and otree (Exp 2) software files.

For Experiment 1, the program was run on z-Tree version 3.5.1.

For Experiment 2, the program was run on otree version 3.0.5.

2) The "Raw Session Files" folder contains all the raw data files generated from the z-Tree (Exp 1) and otree (Exp 2) software. Folders are appropriately named to reflect the dates in which the sessions were run (in YYMMDD format). For Experiment 2, the folder names also indicate the treatments, and "Sessions - ALL" contains the raw data accumulated from all sessions.

3) The "STATA" folder contains the files necessary to replicate all the results reported in the paper (including the Online Appendix).

Within this folder, the "1-RawData" folder contains the essential raw datafiles obtained from the z-Tree and otree session files (see #2).

The "an-paper.do" file in the "2-doFiles" folder contains all the STATA codes required to reproduce all figures, tables, and statistical tests reported in the paper and the Online Appendix.

The "Data" folder contains the processed datasets (in .dta format) made suitable for analysis. "an-paper.do" calls datasets from this folder.
- "Exp-X-cleaned.dta" provides a "wide" format of the dataset. Each row corresponds to an individual participant.
- "Exp-X-cleaned-long.dta" provides a round-level dataset. Each row corresponds to decisions in an individual round by an individual participant.
- "Exp-X-cleaned-long-state.dta" provides a state-level dataset. Each row corresponds to decisions by individuals outcomes, within an individual round, by an individual participant.

Note that all variables in the processed STATA datasets are labelled in a way that are self-explanatory. Use the STATA function "desc" to see all variable labels.

STATA 16 was used for all data analysis. Some installation of commonly used addon packages (e.g., outreg2) may be required.
