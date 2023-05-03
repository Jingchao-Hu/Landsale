clear

import excel using "C:\Users\macbook\Desktop\RA\CityOfficial\City_leaders.xlsx", firstrow 

* unify the format of Term variable and drop uncomplete records
drop if Term ==""
replace Term = subinstr(Term, " ", "", .)
replace Term = subinstr(Term, char(10),"",.)
replace Term = subinstr(Term, char(9),"",.)
replace Term=subinstr(Term,"]","1",.)
drop if substr(Term, 1,1) == "-"
drop if substr(Term, -1,1) == "-"
drop if substr(Term,1,1) !="1" & substr(Term,1,1) !="2"
* generate start_year and end_year variable and change them to numeric type
generate start_year = substr(Term, 1, 4)


generate end_year = substr(Term, strpos(Term, "-") + 1, 4 )

replace end_year = "2022" if substr(end_year, 1,1) != "1" & substr(end_year, 1,1) != "2" //change “至今” to 2022


destring start_year end_year, replace

* change all the position code to 5 or 6
replace Pstcd="6" if Pstcd=="15"
replace Pstcd="5" if Pstcd=="14"
replace Pstcd="6" if Pstcd=="13"
replace Pstcd="5" if Pstcd=="12"
replace Pstcd="6" if Pstcd=="9"
replace Pstcd="5" if Pstcd=="7"
replace Pstcd="6" if Pstcd=="10"
replace Pstcd="5" if Pstcd=="29"
drop if Pstcd=="16"

* generate a variable:term_value=end_year-start_year,replicate every row using term_value
gen term_value=end_year-start_year

expand term_value
bysort Prvn Arcd Pstcd  start_year Offcd: gen year = _n-1+start_year

bysort Prvn Arcd Pstcd  start_year Offcd: gen past_year = _n

drop start_year end_year Term Pstcd

order Prvn Pftn Arcd year Pst Name term_value past_year Pstrm Offcd Gender Eth Bthp Bprvn Bpftn Bcont Bthd Jnpdt Edu_h


save "C:\Users\macbook\Desktop\RA\CityOfficial\output data\newcityofficial.dta",replace

duplicates list Pftn year Pst

