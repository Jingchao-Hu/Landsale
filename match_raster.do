clear
use "C:\Users\macbook\Desktop\RA\cityshape\resultdata\pop_count3.dta"
keep if latitude>3 & latitude<55 & longitude>70 
replace population = 0 if population == -9999
save pop_revisedcount3,replace
use C:\Users\macbook\Desktop\RA\cityshape\resultdata\pop_count4.dta
keep if latitude>3 & latitude<55 & longitude<140 
replace population = 0 if population == -9999
append using pop_revisedcount3.dta
rename latitude y
rename longitude x
order x y population
save C:\Users\macbook\Desktop\RA\cityshape\originaldata\nasa_popcount_2010_raster,replace

clear
use C:\Users\macbook\Desktop\RA\cityshape\originaldata\nasa_popcount_2010_raster.dta
geoinpoly y x using C:\Users\macbook\Desktop\RA\cityshape\originaldata\citycoord.dta
drop if _ID==.
save C:\Users\macbook\Desktop\RA\cityshape\resultdata\matchedcountraster.dta,replace


