** By Chance or by Choice? Biased Attribution of Others' Outcomes when Social Preferences Matter **

/*
Authors:
Nisvan ERKAL
Lata GANGADHARAN
Boon Han KOH
*/

** DO file for analysis in final version of paper **

*******************************************************************************

********** STATISTICS REPORTED IN TEXT **********
*** Note: Any statistics pertaining to regression outputs are reproduced in the next section ***

log using "Logs/InTextStats.log", replace name(InTextStats)

// Section 2.1.2: Average earnings in experiment
use "Data/Exp1-cleaned.dta", clear
sum FinalEarnings

// Section 2.3.1: Spearman's rank correlation coefficients of DG behavior and effort choice
use "Data/Exp1-cleaned-long.dta", clear
foreach x of varlist RA LA HA GA {
spearman DGGivePerc LGHighEff if `x'==1, pw stats(rho p)
}

// Section 2.3.2: Mean interim beliefs by treatment
use "Data/Exp1-cleaned-long.dta", clear
foreach x of varlist RA LA HA GA {
summarize BeliefUnconditional if `x'==1
}

// Section 2.3.2: Pairwise treatment comparisons of mean interim beliefs
* Kolmogorov-Smirnoff tests
use "Data/Exp1-cleaned-long.dta", clear
ksmirnov BeliefUnconditional if RA==1 | LA==1, by(RA) exact // RA vs. LA
ksmirnov BeliefUnconditional if RA==1 | HA==1, by(RA) exact // RA vs. HA
ksmirnov BeliefUnconditional if HA==1 | GA==1, by(GA) exact // GA vs. HA
ksmirnov BeliefUnconditional if RA==1 | GA==1, by(RA) exact // RA vs. GA
* Signed-rank tests
use "Data/Exp1-cleaned.dta", clear
preserve
rename BeliefUnconditional1 BeliefUnconditionalLA1
rename BeliefUnconditional3 BeliefUnconditionalLA2
rename BeliefUnconditional2 BeliefUnconditionalHA1
rename BeliefUnconditional4 BeliefUnconditionalHA2
reshape  long BeliefUnconditionalLA BeliefUnconditionalHA , i(ID) j(Game)
signrank BeliefUnconditional5=BeliefUnconditionalLA // RA vs. LA
signrank BeliefUnconditional5=BeliefUnconditionalHA // RA vs. HA
signrank BeliefUnconditional6=BeliefUnconditionalHA // GA vs. HA
signrank BeliefUnconditional5=BeliefUnconditional6 if Game==1 // RA vs. GA
restore

// Section 2.3.3: Proportion of inconsistent updaters and non-updaters
use "Data/Exp1-cleaned.dta", clear
tab b_Group1 // inconsistent
tab b_Group2 // non-updater
tab b_Group3 // remaining sample

// Section 2.3.3: Footnote 30
use "Data/Exp1-cleaned-long-state.dta", clear
keep if b_Group3==1
reg LogitPosterior i.StateSuccess#c.LogitUnconditional LogitStateGood LogitStateBad, nocon vce(cluster ID)

lincom 0.StateSuccess#LogitUnconditional-1
lincom 1.StateSuccess#LogitUnconditional-1
lincom LogitStateGood-1
lincom LogitStateBad-1
lincom LogitStateGood-LogitStateBad
lincom 1.StateSuccess#LogitUnconditional-0.StateSuccess#LogitUnconditional

capture log close _all

*******************************************************************************

********** MAIN TABLES **********

// Table 2
log using "Logs/Table2.log", replace name(Table2)
use "Data/Exp1-cleaned-long.dta", clear

qui probit LGHighEff DGGivePerc RGInvestPerc i.LA i.HA i.GA i.LGGame i.OrderRAGA i.OrderLAHA, vce(cluster ID)
margins, dydx(*) post
outreg2 using "Tables/Table2", label alpha(0.01, 0.05, 0.10) ctitle("Dependent variable:", "=1 if DM chooses e_H") bdec(3) sdec(3) replace excel tex

capture log close _all

// Table 3
log using "Logs/Table3.log", replace name(Table3)
use "Data/Exp1-cleaned-long.dta", clear
xtset ID

reg BeliefUnconditional i.LA i.HA i.GA RGInvestPerc i.LGGame i.OrderRAGA i.OrderLAHA, vce(cluster ID)
lincom 1.HA-1.GA
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))
outreg2 using "Tables/Table3", label alpha(0.01, 0.05, 0.10) ctitle("Dependent variable: Interim belief") ///
	adds(Test of GA=HA,`est1',t-statistic,`tstat1',p-value,`pval1') ///
	bdec(3) sdec(3) replace tex excel addtext("Order effects","Y","Individual FE","N")
xtreg BeliefUnconditional i.LA i.HA i.GA i.LGGame, fe vce(cluster ID)
lincom 1.HA-1.GA
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))
outreg2 using "Tables/Table3", label alpha(0.01, 0.05, 0.10) ctitle("Dependent variable: Interim belief") ///
	adds(Test of GA=HA,`est1',t-statistic,`tstat1',p-value,`pval1') ///
	bdec(3) sdec(3) append tex excel addtext("Order effects","N","Individual FE","Y")

reg BeliefUnconditional i.LA i.HA i.GA i.LGHighEff RGInvestPerc i.LGGame i.OrderRAGA i.OrderLAHA, vce(cluster ID)
lincom 1.HA-1.GA
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))
outreg2 using "Tables/Table3", label alpha(0.01, 0.05, 0.10) ctitle("Dependent variable: Interim belief") ///
	adds(Test of GA=HA,`est1',t-statistic,`tstat1',p-value,`pval1') ///
	bdec(3) sdec(3) append tex excel addtext("Order effects","Y","Individual FE","N")
xtreg BeliefUnconditional i.LA i.HA i.GA i.LGHighEff i.LGGame, fe vce(cluster ID)
lincom 1.HA-1.GA
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))
outreg2 using "Tables/Table3", label alpha(0.01, 0.05, 0.10) ctitle("Dependent variable: Interim belief") ///
	adds(Test of GA=HA,`est1',t-statistic,`tstat1',p-value,`pval1') ///
	bdec(3) sdec(3) append tex excel addtext("Order effects","N","Individual FE","Y")

capture log close _all

// Table 4
log using "Logs/Table4.log", replace name(Table4)
use "Data/Exp1-cleaned-long-state.dta", clear
keep if b_Group3==1

* Pooled
qui reg LogitPosterior LogitUnconditional LogitStateGood LogitStateBad, nocon vce(cluster ID)

lincom LogitUnconditional-1
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))

lincom LogitStateGood-1
local est2 = r(estimate)
local tstat2 = r(estimate)/r(se)
local pval2 = tprob(r(df), abs(`tstat2'))

lincom LogitStateBad-1
local est3 = r(estimate)
local tstat3 = r(estimate)/r(se)
local pval3 = tprob(r(df), abs(`tstat3'))

lincom LogitStateGood-LogitStateBad
local est4 = r(estimate)
local tstat4 = r(estimate)/r(se)
local pval4 = tprob(r(df), abs(`tstat4'))

outreg2 using "Tables/Table4", label ctitle("Dependent variable: Logit(posterior)", "Pooled") ///
	adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) replace tex excel noas

* Separate by treatments
foreach x of varlist RA LA HA GA {
qui reg LogitPosterior LogitUnconditional LogitStateGood LogitStateBad if `x'==1, nocon vce(cluster ID)

lincom LogitUnconditional-1
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))

lincom LogitStateGood-1
local est2 = r(estimate)
local tstat2 = r(estimate)/r(se)
local pval2 = tprob(r(df), abs(`tstat2'))

lincom LogitStateBad-1
local est3 = r(estimate)
local tstat3 = r(estimate)/r(se)
local pval3 = tprob(r(df), abs(`tstat3'))

lincom LogitStateGood-LogitStateBad
local est4 = r(estimate)
local tstat4 = r(estimate)/r(se)
local pval4 = tprob(r(df), abs(`tstat4'))

outreg2 using "Tables/Table4", label ctitle("Dependent variable: Logit(posterior)", "`x'") ///
	adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) append tex excel noas

}

* Joint test of coefficients across appointment mechanisms
use "Data/Exp1-cleaned-long-state.dta", clear
keep if b_Group3==1
replace Treatment=3 if Treatment==1 // merge LA0 and LA1 together
replace Treatment=4 if Treatment==2 // merge HA0 and HA1 together

reg LogitPosterior i.Treatment#c.LogitUnconditional i.Treatment#c.LogitStateGood i.Treatment#c.LogitStateBad, nocon vce(cluster ID)

testparm Treatment#c.LogitUnconditional, equal
testparm Treatment#c.LogitStateGood, equal
testparm Treatment#c.LogitStateBad, equal

capture log close _all

// Table 5
log using "Logs/Table5.log", replace name(Table5)
use "Data/Exp1-cleaned-long-state.dta", clear
keep if b_Group3==1

local replace replace
foreach x of numlist 0/1{
qui reg LogitPosterior LogitUnconditional LogitStateGood LogitStateBad if LGHighEff==`x', nocon vce(cluster ID)

lincom LogitUnconditional-1
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))

lincom LogitStateGood-1
local est2 = r(estimate)
local tstat2 = r(estimate)/r(se)
local pval2 = tprob(r(df), abs(`tstat2'))

lincom LogitStateBad-1
local est3 = r(estimate)
local tstat3 = r(estimate)/r(se)
local pval3 = tprob(r(df), abs(`tstat3'))

lincom LogitStateGood-LogitStateBad
local est4 = r(estimate)
local tstat4 = r(estimate)/r(se)
local pval4 = tprob(r(df), abs(`tstat4'))

outreg2 using "Tables/Table5", label ctitle("Dependent variable: Logit(posterior)", "Choose high effort = `x'") ///
	adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) `replace' tex excel noas
local replace append
}

reg LogitPosterior i.LGHighEff#c.LogitUnconditional i.LGHighEff#c.LogitStateGood i.LGHighEff#c.LogitStateBad, nocon vce(cluster ID)
testparm LGHighEff#c.LogitUnconditional, equal
testparm LGHighEff#c.LogitStateGood, equal
testparm LGHighEff#c.LogitStateBad, equal

capture log close _all

// Table 6
log using "Logs/Table6.log", replace name(Table6)
use "Data/Exp2-cleaned-long-state.dta", clear
keep if consistent
keep if TreatS

* Round 1 only, by effort choice
local replace replace
foreach x of numlist 0/1 {
    reg logit_posterior logit_prior logit_prob_success logit_prob_failure if high_effort_all==`x' & round==1, nocon vce(cluster id)
	
	lincom logit_prior-1
	local est1 = r(estimate)
	local tstat1 = r(estimate)/r(se)
	local pval1 = tprob(r(df), abs(`tstat1'))

	lincom logit_prob_success-1
	local est2 = r(estimate)
	local tstat2 = r(estimate)/r(se)
	local pval2 = tprob(r(df), abs(`tstat2'))

	lincom logit_prob_failure-1
	local est3 = r(estimate)
	local tstat3 = r(estimate)/r(se)
	local pval3 = tprob(r(df), abs(`tstat3'))

	lincom logit_prob_success-logit_prob_failure
	local est4 = r(estimate)
	local tstat4 = r(estimate)/r(se)
	local pval4 = tprob(r(df), abs(`tstat4'))

	outreg2 using "Tables/Table6", label ctitle("Dependent variable: Logit(posterior)", , "Round 1 only", "High Effort = `x'") ///
		adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) `replace' tex excel noas
local replace append
}

* Joint test of coefficients between columns (1) and (2)
reg logit_posterior i.high_effort_all#c.logit_prior i.high_effort_all#c.logit_prob_success i.high_effort_all#c.logit_prob_failure if round==1, nocon vce(cluster id)
testparm high_effort_all#c.logit_prior, equal
testparm high_effort_all#c.logit_prob_success, equal
testparm high_effort_all#c.logit_prob_failure, equal

* All rounds, by effort choice
local replace append
foreach x of numlist 0/1 {
    reg logit_posterior logit_prior logit_prob_success logit_prob_failure if high_effort_all==`x', nocon vce(cluster id)
	
	lincom logit_prior-1
	local est1 = r(estimate)
	local tstat1 = r(estimate)/r(se)
	local pval1 = tprob(r(df), abs(`tstat1'))

	lincom logit_prob_success-1
	local est2 = r(estimate)
	local tstat2 = r(estimate)/r(se)
	local pval2 = tprob(r(df), abs(`tstat2'))

	lincom logit_prob_failure-1
	local est3 = r(estimate)
	local tstat3 = r(estimate)/r(se)
	local pval3 = tprob(r(df), abs(`tstat3'))

	lincom logit_prob_success-logit_prob_failure
	local est4 = r(estimate)
	local tstat4 = r(estimate)/r(se)
	local pval4 = tprob(r(df), abs(`tstat4'))

	outreg2 using "Tables/Table6", label ctitle("Dependent variable: Logit(posterior)", , "All rounds", "High Effort = `x'") ///
		adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) `replace' tex excel noas
local replace append
}

* Joint test of coefficients between columns (3) and (4)
reg logit_posterior i.high_effort_all#c.logit_prior i.high_effort_all#c.logit_prob_success i.high_effort_all#c.logit_prob_failure, nocon vce(cluster id)
testparm high_effort_all#c.logit_prior, equal
testparm high_effort_all#c.logit_prob_success, equal
testparm high_effort_all#c.logit_prob_failure, equal

capture log close _all

*******************************************************************************

********** MAIN FIGURES **********

// Figure 3
* 3(a)-(d)
use "Data/Exp1-cleaned-long.dta", clear
foreach x of varlist RA LA HA GA {
graph bar if `x'==1, over(LGHighEff) over(DGCat, gap(10) label(labsize(medlarge) angle(forty_five))) asyvars stack ///
	legend(order(1 "Low effort" 2 "High effort") ring(0) bplacement(north)) ///
	ytitle("% total subjects", size(medlarge)) yscale(range(0 50)) ylabel(0(10)50, labsize(medlarge) angle(horizontal)) ///
	bar(1, fcolor(gs8) lcolor(gs8)) bar(2, fcolor(gs0) lcolor(gs0)) ///
	graphregion(color(white)) bgcolor(white)
graph export "Graphs/Figure3-`x'.png", replace
window manage close graph _all
}

// Figure 4
* 4(a)
use "Data/Exp1-cleaned.dta", clear
graph bar, over(LGNomDG, relabel(1 "Lowest DG Giver" 2 "Highest DG Giver" 3 "Indifferent") label(labsize(med)) gap(15)) ///
	ytitle("% total subjects", size(medlarge)) yscale(range(0 90)) ylabel(0(20)90, labsize(medlarge) angle(horizontal)) ///
	blabel(bar, format(%3.1f) size(medlarge)) ///
	bar(1, fcolor(gs6) lcolor(gs12)) ///
	graphregion(color(white)) bgcolor(white)
graph export "Graphs/Figure4a.png", replace
window manage close graph _all
* 4(b)
use "Data/Exp1-cleaned.dta", clear
preserve
gen BeliefNomination1=.
gen BeliefNomination2=.
replace BeliefNomination1=1 if BeliefNomCat==1 | BeliefNomCat==4 | BeliefNomCat==5
replace BeliefNomination1=2 if BeliefNomCat==2 | BeliefNomCat==6
replace BeliefNomination1=3 if BeliefNomCat==3
replace BeliefNomination2=1 if BeliefNomCat==1
replace BeliefNomination2=2 if BeliefNomCat==2 | BeliefNomCat==5
replace BeliefNomination2=3 if BeliefNomCat==3 | BeliefNomCat==4 | BeliefNomCat==6
reshape long BeliefNomination, i(ID)
graph bar, over(BeliefNomination, relabel(1 "Lowest DG Giver" 2 "Highest DG Giver" 3 "Indifferent") label(labsize(med)) gap(15)) ///
	ytitle("% total subjects", size(medlarge)) yscale(range(0 90)) ylabel(0(20)90, labsize(medlarge) angle(horizontal)) ///
	blabel(bar, format(%3.1f) size(medlarge)) ///
	bar(1, fcolor(gs6) lcolor(gs12)) ///
	graphregion(color(white)) bgcolor(white)
graph export "Graphs/Figure4b.png", replace
window manage close graph _all
restore

// Figure 5
* 5(a)-(d)
use "Data/Exp1-cleaned-long.dta", clear
foreach x of varlist LA HA RA GA {
qui summarize BeliefUnconditional if `x'==1, detail
local MUnconditional = r(mean)
twoway (histogram BeliefUnconditional if `x'==1, ///
	width(10) start(0) percent fcolor(gs6) lcolor(gs12)), ///
	ytitle("% subjects", size(medlarge)) xtitle("Interim Belief", size(medlarge)) ///
	yscale(range(0 20)) ylabel(0(5)20, angle(horizontal) labsize(medlarge)) ///
	xscale(range(0 100)) xlabel(0(20)100, labsize(medlarge)) ///
	xline(`MUnconditional', lcolor(black) lpattern(dash)) ///
	graphregion(color(white)) bgcolor(white)
graph export "Graphs/Figure5-`x'.png", replace
window manage close graph _all
}

*******************************************************************************

********** APPENDIX TABLES **********

// Table D.1
log using "Logs/TableD1.log", replace name(TableD1)
use "Data/Exp1-cleaned-long.dta", clear
keep if LGGame==1

probit LGHighEff DGGivePerc RGInvestPerc i.LA i.HA i.GA i.OrderRAGA i.OrderLAHA, vce(cluster ID)
margins, dydx(*) post
outreg2 using "Tables/TableD1", label alpha(0.01, 0.05, 0.10) ctitle("Dependent variable:", "=1 if DM chooses e_H") bdec(3) sdec(3) replace tex excel

capture log close _all

// Table D.2
log using "Logs/TableD2.log", replace name(TableD2)
use "Data/Exp1-cleaned-long.dta", clear
xtset ID
keep if LGGame==1

reg BeliefUnconditional i.LA i.HA i.GA RGInvestPerc i.OrderRAGA i.OrderLAHA, vce(cluster ID)
lincom 1.HA-1.GA
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))
outreg2 using "Tables/TableD2", label alpha(0.01, 0.05, 0.10) ctitle("Dependent variable: Interim belief") ///
	adds(Test of HA=GA,`est1',t-statistic,`tstat1',p-value,`pval1') ///
	bdec(3) sdec(3) replace tex excel addtext("Order effects","Y","Individual FE","N")
xtreg BeliefUnconditional i.LA i.HA i.GA, fe vce(cluster ID)
lincom 1.HA-1.GA
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))
outreg2 using "Tables/TableD2", label alpha(0.01, 0.05, 0.10) ctitle("Dependent variable: Interim belief") ///
	adds(Test of HA=GA,`est1',t-statistic,`tstat1',p-value,`pval1') ///
	bdec(3) sdec(3) append tex excel addtext("Order effects","N","Individual FE","Y")

reg BeliefUnconditional i.LA i.HA i.GA i.LGHighEff RGInvestPerc i.OrderRAGA i.OrderLAHA, vce(cluster ID)
lincom 1.HA-1.GA
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))
outreg2 using "Tables/TableD2", label alpha(0.01, 0.05, 0.10) ctitle("Dependent variable: Interim belief") ///
	adds(Test of HA=GA,`est1',t-statistic,`tstat1',p-value,`pval1') ///
	bdec(3) sdec(3) append tex excel addtext("Order effects","Y","Individual FE","N")
xtreg BeliefUnconditional i.LA i.HA i.GA i.LGHighEff, fe vce(cluster ID)
lincom 1.HA-1.GA
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))
outreg2 using "Tables/TableD2", label alpha(0.01, 0.05, 0.10) ctitle("Dependent variable: Interim belief") ///
	adds(Test of HA=GA,`est1',t-statistic,`tstat1',p-value,`pval1') ///
	bdec(3) sdec(3) append tex excel addtext("Order effects","N","Individual FE","Y")

capture log close _all

// Table D.3
log using "Logs/TableD3.log", replace name(TableD3)
use "Data/Exp1-cleaned-long-state.dta", clear
keep if LGGame==1
keep if b_Group3==1

* Pooled
qui reg LogitPosterior LogitUnconditional LogitStateGood LogitStateBad, nocon vce(cluster ID)

lincom LogitUnconditional-1
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))

lincom LogitStateGood-1
local est2 = r(estimate)
local tstat2 = r(estimate)/r(se)
local pval2 = tprob(r(df), abs(`tstat2'))

lincom LogitStateBad-1
local est3 = r(estimate)
local tstat3 = r(estimate)/r(se)
local pval3 = tprob(r(df), abs(`tstat3'))

lincom LogitStateGood-LogitStateBad
local est4 = r(estimate)
local tstat4 = r(estimate)/r(se)
local pval4 = tprob(r(df), abs(`tstat4'))

outreg2 using "Tables/TableD3", label ctitle("Dependent variable: Logit(posterior)", "Pooled") ///
	adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) replace tex excel noas

* Separate by treatments
foreach x of varlist RA LA HA GA {
qui reg LogitPosterior LogitUnconditional LogitStateGood LogitStateBad if `x'==1, nocon vce(cluster ID)

lincom LogitUnconditional-1
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))

lincom LogitStateGood-1
local est2 = r(estimate)
local tstat2 = r(estimate)/r(se)
local pval2 = tprob(r(df), abs(`tstat2'))

lincom LogitStateBad-1
local est3 = r(estimate)
local tstat3 = r(estimate)/r(se)
local pval3 = tprob(r(df), abs(`tstat3'))

lincom LogitStateGood-LogitStateBad
local est4 = r(estimate)
local tstat4 = r(estimate)/r(se)
local pval4 = tprob(r(df), abs(`tstat4'))

outreg2 using "Tables/TableD3", label ctitle("Dependent variable: Logit(posterior)", "`x'") ///
	adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) append tex excel noas

}

capture log close _all

// Table D.4
log using "Logs/TableD4.log", replace name(TableD4)
use "Data/Exp1-cleaned-long-state.dta", clear
keep if b_Group3==1

ivregress 2sls LogitPosterior LogitStateGood LogitStateBad (LogitUnconditional = i.LA i.HA i.GA), nocons vce(cluster ID)

lincom LogitUnconditional-1
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))

lincom LogitStateGood-1
local est2 = r(estimate)
local tstat2 = r(estimate)/r(se)
local pval2 = tprob(r(df), abs(`tstat2'))

lincom LogitStateBad-1
local est3 = r(estimate)
local tstat3 = r(estimate)/r(se)
local pval3 = tprob(r(df), abs(`tstat3'))

lincom LogitStateGood-LogitStateBad
local est4 = r(estimate)
local tstat4 = r(estimate)/r(se)
local pval4 = tprob(r(df), abs(`tstat4'))

outreg2 using "Tables/TableD4", label ctitle("Dependent variable:", "Logit(posterior)", "Pooled") ///
	bdec(3) sdec(3) replace tex excel noas

ivreg2 LogitPosterior LogitStateGood LogitStateBad (LogitUnconditional = i.LA i.HA i.GA), noc cluster(ID) first orthog(i.LA i.HA i.GA) endog(LogitUnconditional)

capture log close _all

// Table D.5
log using "Logs/TableD5.log", replace name(TableD5)
use "Data/Exp1-cleaned-long-state.dta", clear

* Pooled
qui reg LogitPosterior LogitUnconditional LogitStateGood LogitStateBad, nocon vce(cluster ID)

lincom LogitUnconditional-1
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))

lincom LogitStateGood-1
local est2 = r(estimate)
local tstat2 = r(estimate)/r(se)
local pval2 = tprob(r(df), abs(`tstat2'))

lincom LogitStateBad-1
local est3 = r(estimate)
local tstat3 = r(estimate)/r(se)
local pval3 = tprob(r(df), abs(`tstat3'))

lincom LogitStateGood-LogitStateBad
local est4 = r(estimate)
local tstat4 = r(estimate)/r(se)
local pval4 = tprob(r(df), abs(`tstat4'))

outreg2 using "Tables/TableD5", label ctitle("Dependent variable: Logit(posterior)", "Pooled") ///
	adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) replace tex excel noas

* Separate by treatments
foreach x of varlist RA LA HA GA {
qui reg LogitPosterior LogitUnconditional LogitStateGood LogitStateBad if `x'==1, nocon vce(cluster ID)

lincom LogitUnconditional-1
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))

lincom LogitStateGood-1
local est2 = r(estimate)
local tstat2 = r(estimate)/r(se)
local pval2 = tprob(r(df), abs(`tstat2'))

lincom LogitStateBad-1
local est3 = r(estimate)
local tstat3 = r(estimate)/r(se)
local pval3 = tprob(r(df), abs(`tstat3'))

lincom LogitStateGood-LogitStateBad
local est4 = r(estimate)
local tstat4 = r(estimate)/r(se)
local pval4 = tprob(r(df), abs(`tstat4'))

outreg2 using "Tables/TableD5", label ctitle("Dependent variable: Logit(posterior)", "`x'") ///
	adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) append tex excel noas

}

capture log close _all

// Table D.6
log using "Logs/TableD6.log", replace name(TableD6)
use "Data/Exp1-cleaned-long-state.dta", clear

* Column 1 - drop a round if there are no updates in either direction
preserve
bys ID Treatment: egen BeliefNoneTotalRound=sum(BeliefNone)
drop if BeliefNoneTotalRound==2

reg LogitPosterior LogitUnconditional LogitStateGood LogitStateBad, nocon vce(cluster ID)

lincom LogitUnconditional-1
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))

lincom LogitStateGood-1
local est2 = r(estimate)
local tstat2 = r(estimate)/r(se)
local pval2 = tprob(r(df), abs(`tstat2'))

lincom LogitStateBad-1
local est3 = r(estimate)
local tstat3 = r(estimate)/r(se)
local pval3 = tprob(r(df), abs(`tstat3'))

lincom LogitStateGood-LogitStateBad
local est4 = r(estimate)
local tstat4 = r(estimate)/r(se)
local pval4 = tprob(r(df), abs(`tstat4'))

outreg2 using "Tables/TableD6", label ctitle("Dependent variable: Logit(posterior)", "Include only subject-rounds with updates") ///
	adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) replace tex excel noas
restore

* Column 2 - include only subjects with updates in all rounds
preserve
bys ID: egen BeliefNoneTotalRound=sum(BeliefNone)
drop if BeliefNoneTotalRound>=1

reg LogitPosterior LogitUnconditional LogitStateGood LogitStateBad, nocon vce(cluster ID)

lincom LogitUnconditional-1
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))

lincom LogitStateGood-1
local est2 = r(estimate)
local tstat2 = r(estimate)/r(se)
local pval2 = tprob(r(df), abs(`tstat2'))

lincom LogitStateBad-1
local est3 = r(estimate)
local tstat3 = r(estimate)/r(se)
local pval3 = tprob(r(df), abs(`tstat3'))

lincom LogitStateGood-LogitStateBad
local est4 = r(estimate)
local tstat4 = r(estimate)/r(se)
local pval4 = tprob(r(df), abs(`tstat4'))

outreg2 using "Tables/TableD6", label ctitle("Dependent variable: Logit(posterior)", "Include only subjects with updates in all rounds") ///
	adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) append tex excel noas
restore

capture log close _all

// Table D.7
log using "Logs/TableD7.log", replace name(TableD7)
use "Data/Exp1-cleaned-long-state.dta", clear
drop if b_Group2

local replace replace
foreach x of numlist 1/10 {
reg LogitPosterior LogitUnconditional LogitStateGood LogitStateBad if BeliefIncTotal<`x', nocon vce(cluster ID)

lincom LogitUnconditional-1
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))

lincom LogitStateGood-1
local est2 = r(estimate)
local tstat2 = r(estimate)/r(se)
local pval2 = tprob(r(df), abs(`tstat2'))

lincom LogitStateBad-1
local est3 = r(estimate)
local tstat3 = r(estimate)/r(se)
local pval3 = tprob(r(df), abs(`tstat3'))

lincom LogitStateGood-LogitStateBad
local est4 = r(estimate)
local tstat4 = r(estimate)/r(se)
local pval4 = tprob(r(df), abs(`tstat4'))

outreg2 using "Tables/TableD7", label ctitle("Dependent variable: Logit(posterior)", ">= `x'") ///
	adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) `replace' tex excel noas
local replace append
}

capture log close _all

// Table D.8
log using "Logs/TableD8.log", replace name(TableD8)
use "Data/Exp1-cleaned-long-state.dta", clear
keep if b_Group3==1

fmm 2, vce(cluster ID) iterate(100): regress LogitPosterior LogitUnconditional LogitStateGood LogitStateBad, nocons
estat lcprob
estat ic
estimates store fmm2

lincom 1.Class#LogitUnconditional-1
lincom 1.Class#LogitStateGood-1
lincom 1.Class#LogitStateBad-1
lincom 1.Class#LogitStateGood-1.Class#LogitStateBad

lincom 2.Class#LogitUnconditional-1
lincom 2.Class#LogitStateGood-1
lincom 2.Class#LogitStateBad-1
lincom 2.Class#LogitStateGood-2.Class#LogitStateBad

outreg2 using "Tables/TableD8", label ctitle("Dependent variable: Logit(posterior)", "2-Component Model") bdec(3) sdec(3) replace tex excel noas

fmm 3, vce(cluster ID) iterate(100): regress LogitPosterior LogitUnconditional LogitStateGood LogitStateBad, nocons
estat lcprob
estat ic
estimates store fmm3

lincom 1.Class#LogitUnconditional-1
lincom 1.Class#LogitStateGood-1
lincom 1.Class#LogitStateBad-1
lincom 1.Class#LogitStateGood-1.Class#LogitStateBad

lincom 2.Class#LogitUnconditional-1
lincom 2.Class#LogitStateGood-1
lincom 2.Class#LogitStateBad-1
lincom 2.Class#LogitStateGood-2.Class#LogitStateBad

lincom 3.Class#LogitUnconditional-1
lincom 3.Class#LogitStateGood-1
lincom 3.Class#LogitStateBad-1
lincom 3.Class#LogitStateGood-3.Class#LogitStateBad

outreg2 using "Tables/TableD8", label ctitle("Dependent variable: Logit(posterior)", "3-Component Model") bdec(3) sdec(3) append tex excel noas

capture log close _all

// Table D.9
log using "Logs/TableD9.log", replace name(TableD9)
use "Data/Exp2-cleaned.dta", clear

append using "Data/Exp1-cleaned.dta"
replace treatment=3 if treatment==.
label define treatment_lbl 1 "Exp 2: Treatment S", replace
label define treatment_lbl 2 "Exp 2: Treatment D", add
label define treatment_lbl 3 "Exp 1", add
label values treatment treatment_lbl
gen lab=1 if treatment==3
replace lab=0 if treatment!=3

replace age=surveyAge if lab
replace female=surveyFemale if lab
replace economics=surveyEconomics if lab
replace undergraduate=surveyUG if lab
replace postgraduate=surveyPG if lab
replace australian=surveyAustralian if lab
replace australian=0 if lab & surveyAustralian!=1
replace past_experiments=surveyPastExp if lab
replace dg_gave_perc=DGGivePerc if lab
replace risk_invest_perc=RGInvestPerc if lab

estpost tabstat age female economics postgraduate australian past_experiments dg_gave_perc risk_invest_perc, ///
	statistics(mean count sd semean) columns(statistics) by(treatment)
esttab using "Tables/TableD9", main(mean %8.3f) aux(sd %8.3f) obslast label lines nostar unstack nonote nomtitle nonumber rtf ///
	title("Subjects' characteristics in Experiment 1 and Experiment 2") brackets replace
esttab using "Tables/TableD9", main(mean %8.3f) aux(sd %8.3f) obslast label lines nostar unstack nonote nomtitle nonumber tex ///
	title("Subjects' characteristics in Experiment 1 and Experiment 2") brackets replace

mvreg age female economics postgraduate australian past_experiments dg_gave_perc risk_invest_perc = i.lab
mvtest means age female economics postgraduate australian past_experiments dg_gave_perc risk_invest_perc, by(treatment)

mvreg age female economics postgraduate australian past_experiments dg_gave_perc risk_invest_perc = i.TreatS if lab!=1
mvtest means age female economics postgraduate australian past_experiments dg_gave_perc risk_invest_perc if lab!=1, by(TreatS)

capture log close _all

// Table D.10
log using "Logs/TableD10.log", replace name(TableD10)
use "Data/Exp2-cleaned-long.dta", clear

probit high_effort_hyp dg_gave_perc risk_invest_perc i.param if round==1, vce(cluster id)
margins, dydx(*) post
outreg2 using "Tables/TableD10", label alpha(0.01, 0.05, 0.10) ctitle("Dependent variable:", "=1 if member would have chosen e_H as DM", "Round 1 only") bdec(3) sdec(3) replace tex excel

probit high_effort_hyp dg_gave_perc risk_invest_perc i.param i.round, vce(cluster id)
margins, dydx(*) post
outreg2 using "Tables/TableD10", label alpha(0.01, 0.05, 0.10) ctitle("Dependent variable:", "=1 if member would have chosen e_H as DM", "All rounds") bdec(3) sdec(3) append tex excel

capture log close _all

// Table D.11
log using "Logs/TableD11.log", replace name(TableD11)
use "Data/Exp2-cleaned-long-state.dta", clear
keep if consistent

* Treatment S, by effort choice
local replace replace
foreach x of numlist 0/1 {
    reg logit_posterior logit_prior logit_prob_success logit_prob_failure if high_effort_all==`x' & TreatS==1, nocon vce(cluster id)
	
	lincom logit_prior-1
	local est1 = r(estimate)
	local tstat1 = r(estimate)/r(se)
	local pval1 = tprob(r(df), abs(`tstat1'))

	lincom logit_prob_success-1
	local est2 = r(estimate)
	local tstat2 = r(estimate)/r(se)
	local pval2 = tprob(r(df), abs(`tstat2'))

	lincom logit_prob_failure-1
	local est3 = r(estimate)
	local tstat3 = r(estimate)/r(se)
	local pval3 = tprob(r(df), abs(`tstat3'))

	lincom logit_prob_success-logit_prob_failure
	local est4 = r(estimate)
	local tstat4 = r(estimate)/r(se)
	local pval4 = tprob(r(df), abs(`tstat4'))

	outreg2 using "Tables/TableD11", label ctitle("Dependent variable: Logit(posterior)", , "Treatment S", "High Effort = `x'") ///
		adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) `replace' tex excel noas
local replace append
}

* Treatment D, by effort choice
local replace append
foreach x of numlist 0/1 {
    reg logit_posterior logit_prior logit_prob_success logit_prob_failure if high_effort_all==`x' & TreatD==1, nocon vce(cluster id)
	
	lincom logit_prior-1
	local est1 = r(estimate)
	local tstat1 = r(estimate)/r(se)
	local pval1 = tprob(r(df), abs(`tstat1'))

	lincom logit_prob_success-1
	local est2 = r(estimate)
	local tstat2 = r(estimate)/r(se)
	local pval2 = tprob(r(df), abs(`tstat2'))

	lincom logit_prob_failure-1
	local est3 = r(estimate)
	local tstat3 = r(estimate)/r(se)
	local pval3 = tprob(r(df), abs(`tstat3'))

	lincom logit_prob_success-logit_prob_failure
	local est4 = r(estimate)
	local tstat4 = r(estimate)/r(se)
	local pval4 = tprob(r(df), abs(`tstat4'))

	outreg2 using "Tables/TableD11", label ctitle("Dependent variable: Logit(posterior)", , "Treatment S", "High Effort = `x'") ///
		adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) `replace' tex excel noas
local replace append
}

* Joint test of coefficients between columns (1) and (2)
reg logit_posterior i.high_effort_all#c.logit_prior i.high_effort_all#c.logit_prob_success i.high_effort_all#c.logit_prob_failure if TreatS==1, nocon vce(cluster id)
testparm high_effort_all#c.logit_prior, equal
testparm high_effort_all#c.logit_prob_success, equal
testparm high_effort_all#c.logit_prob_failure, equal

* Joint test of coefficients between columns (3) and (4)
reg logit_posterior i.high_effort_all#c.logit_prior i.high_effort_all#c.logit_prob_success i.high_effort_all#c.logit_prob_failure if TreatD==1, nocon vce(cluster id)
testparm high_effort_all#c.logit_prior, equal
testparm high_effort_all#c.logit_prob_success, equal
testparm high_effort_all#c.logit_prob_failure, equal

* Joint test of coefficients between columns (1) and (3)
reg logit_posterior i.TreatD#c.logit_prior i.TreatD#c.logit_prob_success i.TreatD#c.logit_prob_failure if high_effort_all==0, nocon vce(cluster id)
testparm TreatD#c.logit_prior, equal
testparm TreatD#c.logit_prob_success, equal
testparm TreatD#c.logit_prob_failure, equal

* Joint test of coefficients between columns (2) and (4)
reg logit_posterior i.TreatD#c.logit_prior i.TreatD#c.logit_prob_success i.TreatD#c.logit_prob_failure if high_effort_all==1, nocon vce(cluster id)
testparm TreatD#c.logit_prior, equal
testparm TreatD#c.logit_prob_success, equal
testparm TreatD#c.logit_prob_failure, equal

capture log close _all

// Table D.12
log using "Logs/TableD12.log", replace name(TableD12)
use "Data/Exp2-cleaned-long-state.dta", clear
keep if consistent

* Treatment S, Treatment D
local replace replace
foreach x in S D {
    reg logit_posterior logit_prior logit_prob_success logit_prob_failure if Treat`x'==1, nocon vce(cluster id)
	
	lincom logit_prior-1
	local est1 = r(estimate)
	local tstat1 = r(estimate)/r(se)
	local pval1 = tprob(r(df), abs(`tstat1'))

	lincom logit_prob_success-1
	local est2 = r(estimate)
	local tstat2 = r(estimate)/r(se)
	local pval2 = tprob(r(df), abs(`tstat2'))

	lincom logit_prob_failure-1
	local est3 = r(estimate)
	local tstat3 = r(estimate)/r(se)
	local pval3 = tprob(r(df), abs(`tstat3'))

	lincom logit_prob_success-logit_prob_failure
	local est4 = r(estimate)
	local tstat4 = r(estimate)/r(se)
	local pval4 = tprob(r(df), abs(`tstat4'))

	outreg2 using "Tables/TableD12", label ctitle("Dependent variable: Logit(posterior)", "Treatment `x'") ///
		adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) `replace' tex excel noas
local replace append
}

* Treatment S + Treatment D
reg logit_posterior logit_prior logit_prob_success logit_prob_failure, nocon vce(cluster id)

lincom logit_prior-1
local est1 = r(estimate)
local tstat1 = r(estimate)/r(se)
local pval1 = tprob(r(df), abs(`tstat1'))

lincom logit_prob_success-1
local est2 = r(estimate)
local tstat2 = r(estimate)/r(se)
local pval2 = tprob(r(df), abs(`tstat2'))

lincom logit_prob_failure-1
local est3 = r(estimate)
local tstat3 = r(estimate)/r(se)
local pval3 = tprob(r(df), abs(`tstat3'))

lincom logit_prob_success-logit_prob_failure
local est4 = r(estimate)
local tstat4 = r(estimate)/r(se)
local pval4 = tprob(r(df), abs(`tstat4'))

outreg2 using "Tables/TableD12", label ctitle("Dependent variable: Logit(posterior)", "S + D") ///
	adds(delta,`est1',t-stat_delta,`tstat1',p-val_delta,`pval1', ///
	gammaG,`est2',t-stat_gammaG,`tstat2',p-val_gammaG,`pval2', ///
	gammaB,`est3',t-stat_gammaB,`tstat3',p-val_gammaB,`pval3', ///
	gammaG=gammaB,`est4',t-stat_gammaG=gammaB,`tstat4',p-val_gammaG=gammaB,`pval4') bdec(3) sdec(3) append tex excel noas

* Joint test of coefficients between columns (1) and (2)
reg logit_posterior i.TreatD#c.logit_prior i.TreatD#c.logit_prob_success i.TreatD#c.logit_prob_failure, nocon vce(cluster id)
testparm TreatD#c.logit_prior, equal
testparm TreatD#c.logit_prob_success, equal
testparm TreatD#c.logit_prob_failure, equal

* Joint test of coefficients between columns (3) and Exp 1
use "Data/Exp2-cleaned-long-state.dta", clear
append using "Data/Exp1-cleaned-long-state.dta"
keep if consistent==1 | b_Group3==1

replace logit_prior=LogitUnconditional if b_Group==3
replace logit_posterior=LogitPosterior if b_Group==3
replace logit_prob_success=LogitStateGood if b_Group==3
replace logit_prob_failure=LogitStateBad if b_Group==3

replace id=ID if b_Group3==1

replace treatment=3 if treatment==.
gen lab=1 if treatment==3
replace lab=0 if treatment!=3

reg logit_posterior i.lab#c.logit_prior i.lab#c.logit_prob_success i.lab#c.logit_prob_failure, nocon vce(cluster id)
testparm lab#c.logit_prior, equal
testparm lab#c.logit_prob_success, equal
testparm lab#c.logit_prob_failure, equal

capture log close _all

*******************************************************************************

********** APPENDIX FIGURES **********

// Figure D.1
use "Data\Exp1-cleaned-long-state.dta", clear
* D.1(a)
twoway histogram BeliefIncTotal if Treatment==1 & StateSuccess==1, discrete width(1) start(0) percent ///
	yscale(range(0 60)) ylabel(0(20)60, labsize(medlarge) angle(horizontal)) ///
	xscale(range(0 12.5)) xlabel(0(1)12.5, labsize(medlarge)) ///
	xtitle("# updates in wrong direction", size(medlarge)) ytitle("% subjects", size(medlarge)) ///
	graphregion(color(white)) bgcolor(white) fcolor(gs6) lcolor(gs12)
graph export "Graphs/FigureD1a.png", replace
* D.1(b)
twoway histogram BeliefNoneTotal if Treatment==1 & StateSuccess==1, discrete width(1) start(0) percent ///
	yscale(range(0 60)) ylabel(0(20)60, labsize(medlarge) angle(horizontal)) ///
	xscale(range(0 12.5)) xlabel(0(1)12.5, labsize(medlarge)) ///
	xtitle("# non-updates", size(medlarge)) ytitle("% subjects", size(medlarge)) ///
	graphregion(color(white)) bgcolor(white) fcolor(gs6) lcolor(gs12)
graph export "Graphs/FigureD1b.png", replace
window manage close graph _all